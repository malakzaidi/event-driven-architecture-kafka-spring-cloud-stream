"""
Pneumonia Classifier Model Architecture
Uses Transfer Learning with ResNet18
"""
import torch
import torch.nn as nn
import torchvision.models as models
from config import NUM_CLASSES


class PneumoniaClassifier(nn.Module):
    """
    CNN model for pneumonia classification using transfer learning
    """
    def __init__(self, num_classes=NUM_CLASSES, pretrained=True):
        super(PneumoniaClassifier, self).__init__()
        
        # Load pre-trained ResNet18
        self.resnet = models.resnet18(pretrained=pretrained)
        
        # Freeze early layers (optional - can be unfrozen for fine-tuning)
        for param in list(self.resnet.parameters())[:-10]:
            param.requires_grad = False
        
        # Get the number of features from the last layer
        num_features = self.resnet.fc.in_features
        
        # Replace the final fully connected layer
        self.resnet.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x):
        """
        Forward pass
        Args:
            x: Input tensor of shape (batch_size, 3, 224, 224)
        Returns:
            Output tensor of shape (batch_size, num_classes)
        """
        return self.resnet(x)


class SimpleCNN(nn.Module):
    """
    Simple CNN architecture (alternative to transfer learning)
    """
    def __init__(self, num_classes=NUM_CLASSES):
        super(SimpleCNN, self).__init__()
        
        self.features = nn.Sequential(
            # Conv Block 1
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Conv Block 2
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Conv Block 3
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Conv Block 4
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 14 * 14, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
    
    def forward(self, x):
        """
        Forward pass
        Args:
            x: Input tensor of shape (batch_size, 3, 224, 224)
        Returns:
            Output tensor of shape (batch_size, num_classes)
        """
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x


def get_model(model_type='resnet', num_classes=NUM_CLASSES, pretrained=True):
    """
    Factory function to get the model
    
    Args:
        model_type: Type of model ('resnet' or 'simple')
        num_classes: Number of output classes
        pretrained: Whether to use pre-trained weights (for ResNet)
    
    Returns:
        Model instance
    """
    if model_type == 'resnet':
        return PneumoniaClassifier(num_classes=num_classes, pretrained=pretrained)
    elif model_type == 'simple':
        return SimpleCNN(num_classes=num_classes)
    else:
        raise ValueError(f"Unknown model type: {model_type}")


def count_parameters(model):
    """
    Count the number of trainable parameters in the model
    
    Args:
        model: PyTorch model
    
    Returns:
        Number of trainable parameters
    """
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


if __name__ == "__main__":
    # Test the model
    print("Testing Pneumonia Classifier Model...")
    
    # Create model
    model = get_model(model_type='resnet')
    print(f"\nModel Architecture:\n{model}")
    
    # Count parameters
    num_params = count_parameters(model)
    print(f"\nNumber of trainable parameters: {num_params:,}")
    
    # Test forward pass
    dummy_input = torch.randn(1, 3, 224, 224)
    output = model(dummy_input)
    print(f"\nInput shape: {dummy_input.shape}")
    print(f"Output shape: {output.shape}")
    
    # Test with batch
    batch_input = torch.randn(4, 3, 224, 224)
    batch_output = model(batch_input)
    print(f"\nBatch input shape: {batch_input.shape}")
    print(f"Batch output shape: {batch_output.shape}")
    
    print("\n✅ Model test completed successfully!")
