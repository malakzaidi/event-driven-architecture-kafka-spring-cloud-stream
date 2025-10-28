"""
Training script for Pneumonia Classifier
"""
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset, random_split
from torchvision import transforms
from PIL import Image
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import time

from model import get_model, count_parameters
from config import *


class PneumoniaDataset(Dataset):
    """
    Custom Dataset for Pneumonia X-ray images
    Expected directory structure:
    data/
        train/
            NORMAL/
                *.jpeg
            PNEUMONIA/
                *.jpeg
        test/
            NORMAL/
            PNEUMONIA/
    """
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.images = []
        self.labels = []
        
        # Load images and labels
        for class_idx, class_name in enumerate(CLASS_NAMES):
            class_dir = os.path.join(root_dir, class_name.upper())
            if not os.path.exists(class_dir):
                print(f"Warning: Directory {class_dir} does not exist")
                continue
            
            for img_name in os.listdir(class_dir):
                if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(class_dir, img_name)
                    self.images.append(img_path)
                    self.labels.append(class_idx)
        
        print(f"Loaded {len(self.images)} images from {root_dir}")
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        label = self.labels[idx]
        
        # Load image
        image = Image.open(img_path).convert('RGB')
        
        # Apply transforms
        if self.transform:
            image = self.transform(image)
        
        return image, label


def get_transforms(augment=True):
    """
    Get image transforms for training and validation
    
    Args:
        augment: Whether to apply data augmentation
    
    Returns:
        Transform pipeline
    """
    if augment:
        return transforms.Compose([
            transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            transforms.RandomRotation(AUGMENTATION['rotation_range']),
            transforms.RandomHorizontalFlip(),
            transforms.RandomAffine(
                degrees=0,
                translate=(AUGMENTATION['width_shift_range'], 
                          AUGMENTATION['height_shift_range']),
                scale=(1-AUGMENTATION['zoom_range'], 1+AUGMENTATION['zoom_range'])
            ),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    else:
        return transforms.Compose([
            transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])


def train_epoch(model, dataloader, criterion, optimizer, device):
    """
    Train for one epoch
    
    Returns:
        Average loss and accuracy
    """
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(dataloader, desc='Training')
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)
        
        # Zero gradients
        optimizer.zero_grad()
        
        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        # Statistics
        running_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        
        # Update progress bar
        pbar.set_postfix({
            'loss': f'{loss.item():.4f}',
            'acc': f'{100 * correct / total:.2f}%'
        })
    
    epoch_loss = running_loss / len(dataloader)
    epoch_acc = 100 * correct / total
    
    return epoch_loss, epoch_acc


def validate(model, dataloader, criterion, device):
    """
    Validate the model
    
    Returns:
        Average loss and accuracy
    """
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        pbar = tqdm(dataloader, desc='Validation')
        for images, labels in pbar:
            images, labels = images.to(device), labels.to(device)
            
            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # Statistics
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            
            # Update progress bar
            pbar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'acc': f'{100 * correct / total:.2f}%'
            })
    
    epoch_loss = running_loss / len(dataloader)
    epoch_acc = 100 * correct / total
    
    return epoch_loss, epoch_acc, all_preds, all_labels


def plot_training_history(train_losses, val_losses, train_accs, val_accs, save_path='training_history.png'):
    """
    Plot training history
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Loss plot
    ax1.plot(train_losses, label='Train Loss')
    ax1.plot(val_losses, label='Val Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('Training and Validation Loss')
    ax1.legend()
    ax1.grid(True)
    
    # Accuracy plot
    ax2.plot(train_accs, label='Train Acc')
    ax2.plot(val_accs, label='Val Acc')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.set_title('Training and Validation Accuracy')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Training history saved to {save_path}")


def train_model(train_dir, val_dir=None, model_type='resnet', num_epochs=NUM_EPOCHS):
    """
    Main training function
    
    Args:
        train_dir: Path to training data directory
        val_dir: Path to validation data directory (optional)
        model_type: Type of model to use
        num_epochs: Number of training epochs
    """
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Create datasets
    print("\nLoading datasets...")
    train_transform = get_transforms(augment=True)
    val_transform = get_transforms(augment=False)
    
    train_dataset = PneumoniaDataset(train_dir, transform=train_transform)
    
    if val_dir:
        val_dataset = PneumoniaDataset(val_dir, transform=val_transform)
    else:
        # Split training data into train and validation
        train_size = int(0.8 * len(train_dataset))
        val_size = len(train_dataset) - train_size
        train_dataset, val_dataset = random_split(
            train_dataset, 
            [train_size, val_size],
            generator=torch.Generator().manual_seed(RANDOM_SEED)
        )
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset, 
        batch_size=BATCH_SIZE, 
        shuffle=True, 
        num_workers=4
    )
    val_loader = DataLoader(
        val_dataset, 
        batch_size=BATCH_SIZE, 
        shuffle=False, 
        num_workers=4
    )
    
    print(f"Training samples: {len(train_dataset)}")
    print(f"Validation samples: {len(val_dataset)}")
    
    # Create model
    print(f"\nCreating {model_type} model...")
    model = get_model(model_type=model_type, num_classes=NUM_CLASSES)
    model = model.to(device)
    
    num_params = count_parameters(model)
    print(f"Number of trainable parameters: {num_params:,}")
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=3, verbose=True
    )
    
    # Training loop
    print(f"\nStarting training for {num_epochs} epochs...")
    train_losses, val_losses = [], []
    train_accs, val_accs = [], []
    best_val_acc = 0.0
    
    start_time = time.time()
    
    for epoch in range(num_epochs):
        print(f"\n{'='*60}")
        print(f"Epoch {epoch+1}/{num_epochs}")
        print(f"{'='*60}")
        
        # Train
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        train_losses.append(train_loss)
        train_accs.append(train_acc)
        
        # Validate
        val_loss, val_acc, val_preds, val_labels = validate(model, val_loader, criterion, device)
        val_losses.append(val_loss)
        val_accs.append(val_acc)
        
        # Learning rate scheduling
        scheduler.step(val_loss)
        
        # Print epoch summary
        print(f"\nEpoch {epoch+1} Summary:")
        print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        print(f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            os.makedirs(MODEL_DIR, exist_ok=True)
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
                'val_loss': val_loss,
            }, MODEL_PATH)
            print(f"✅ Best model saved with validation accuracy: {val_acc:.2f}%")
    
    training_time = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"Training completed in {training_time/60:.2f} minutes")
    print(f"Best validation accuracy: {best_val_acc:.2f}%")
    print(f"{'='*60}")
    
    # Plot training history
    plot_training_history(train_losses, val_losses, train_accs, val_accs)
    
    # Print classification report
    print("\nFinal Validation Classification Report:")
    print(classification_report(val_labels, val_preds, target_names=CLASS_NAMES))
    
    # Confusion matrix
    cm = confusion_matrix(val_labels, val_preds)
    print("\nConfusion Matrix:")
    print(cm)
    
    return model


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Train Pneumonia Classifier')
    parser.add_argument('--train_dir', type=str, default='data/train',
                       help='Path to training data directory')
    parser.add_argument('--val_dir', type=str, default=None,
                       help='Path to validation data directory')
    parser.add_argument('--model_type', type=str, default='resnet',
                       choices=['resnet', 'simple'],
                       help='Type of model to use')
    parser.add_argument('--epochs', type=int, default=NUM_EPOCHS,
                       help='Number of training epochs')
    
    args = parser.parse_args()
    
    # Check if training directory exists
    if not os.path.exists(args.train_dir):
        print(f"Error: Training directory '{args.train_dir}' does not exist!")
        print("\nExpected directory structure:")
        print("data/")
        print("  train/")
        print("    NORMAL/")
        print("      *.jpeg")
        print("    PNEUMONIA/")
        print("      *.jpeg")
        exit(1)
    
    # Train model
    train_model(
        train_dir=args.train_dir,
        val_dir=args.val_dir,
        model_type=args.model_type,
        num_epochs=args.epochs
    )
