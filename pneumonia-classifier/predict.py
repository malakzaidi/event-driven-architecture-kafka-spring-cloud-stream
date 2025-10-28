"""
Inference module for Pneumonia Classifier
"""
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import numpy as np
import os

from model import get_model
from config import *


class PneumoniaPredictor:
    """
    Predictor class for pneumonia classification
    """
    def __init__(self, model_path=MODEL_PATH, device=None):
        """
        Initialize the predictor
        
        Args:
            model_path: Path to the trained model
            device: Device to run inference on (cuda/cpu)
        """
        self.device = device if device else torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.transform = self._get_transform()
        
        # Load model if path exists
        if os.path.exists(model_path):
            self.load_model(model_path)
        else:
            print(f"Warning: Model file not found at {model_path}")
            print("Please train the model first or provide a valid model path")
    
    def _get_transform(self):
        """
        Get image preprocessing transform
        """
        return transforms.Compose([
            transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    
    def load_model(self, model_path):
        """
        Load trained model from checkpoint
        
        Args:
            model_path: Path to model checkpoint
        """
        print(f"Loading model from {model_path}...")
        
        # Create model
        self.model = get_model(model_type='resnet', num_classes=NUM_CLASSES)
        
        # Load checkpoint
        checkpoint = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        
        # Move to device and set to eval mode
        self.model = self.model.to(self.device)
        self.model.eval()
        
        print(f"✅ Model loaded successfully!")
        if 'val_acc' in checkpoint:
            print(f"Model validation accuracy: {checkpoint['val_acc']:.2f}%")
    
    def preprocess_image(self, image_path):
        """
        Preprocess image for inference
        
        Args:
            image_path: Path to image file or PIL Image
        
        Returns:
            Preprocessed image tensor
        """
        # Load image
        if isinstance(image_path, str):
            image = Image.open(image_path).convert('RGB')
        elif isinstance(image_path, Image.Image):
            image = image.convert('RGB')
        else:
            raise ValueError("image_path must be a file path or PIL Image")
        
        # Apply transforms
        image_tensor = self.transform(image)
        
        # Add batch dimension
        image_tensor = image_tensor.unsqueeze(0)
        
        return image_tensor
    
    def predict(self, image_path, return_probabilities=True):
        """
        Make prediction on a single image
        
        Args:
            image_path: Path to image file or PIL Image
            return_probabilities: Whether to return class probabilities
        
        Returns:
            Dictionary containing prediction results
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Please load a model first.")
        
        # Preprocess image
        image_tensor = self.preprocess_image(image_path)
        image_tensor = image_tensor.to(self.device)
        
        # Make prediction
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probabilities = F.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        # Get results
        predicted_class = predicted.item()
        predicted_label = CLASS_NAMES[predicted_class]
        confidence_score = confidence.item()
        
        result = {
            'predicted_class': predicted_class,
            'predicted_label': predicted_label,
            'confidence': confidence_score,
        }
        
        if return_probabilities:
            class_probabilities = {
                CLASS_NAMES[i]: probabilities[0][i].item() 
                for i in range(NUM_CLASSES)
            }
            result['probabilities'] = class_probabilities
        
        return result
    
    def predict_batch(self, image_paths):
        """
        Make predictions on multiple images
        
        Args:
            image_paths: List of image paths
        
        Returns:
            List of prediction results
        """
        results = []
        for image_path in image_paths:
            result = self.predict(image_path)
            results.append(result)
        return results
    
    def explain_prediction(self, image_path):
        """
        Get detailed explanation of prediction
        
        Args:
            image_path: Path to image file
        
        Returns:
            Formatted explanation string
        """
        result = self.predict(image_path)
        
        explanation = f"""
╔══════════════════════════════════════════════════════════╗
║           PNEUMONIA CLASSIFICATION RESULT                ║
╚══════════════════════════════════════════════════════════╝

Prediction: {result['predicted_label']}
Confidence: {result['confidence']*100:.2f}%

Class Probabilities:
"""
        for class_name, prob in result['probabilities'].items():
            bar_length = int(prob * 40)
            bar = '█' * bar_length + '░' * (40 - bar_length)
            explanation += f"  {class_name:12s} [{bar}] {prob*100:.2f}%\n"
        
        # Add interpretation
        explanation += "\nInterpretation:\n"
        if result['predicted_label'] == 'Pneumonia':
            if result['confidence'] > 0.9:
                explanation += "  ⚠️  HIGH confidence pneumonia detection.\n"
                explanation += "  Recommendation: Immediate medical consultation advised.\n"
            elif result['confidence'] > 0.7:
                explanation += "  ⚠️  MODERATE confidence pneumonia detection.\n"
                explanation += "  Recommendation: Medical consultation recommended.\n"
            else:
                explanation += "  ⚠️  LOW confidence pneumonia detection.\n"
                explanation += "  Recommendation: Further examination may be needed.\n"
        else:
            if result['confidence'] > 0.9:
                explanation += "  ✅ HIGH confidence normal classification.\n"
                explanation += "  No signs of pneumonia detected.\n"
            elif result['confidence'] > 0.7:
                explanation += "  ✅ MODERATE confidence normal classification.\n"
                explanation += "  Low probability of pneumonia.\n"
            else:
                explanation += "  ⚠️  LOW confidence normal classification.\n"
                explanation += "  Recommendation: Further examination may be needed.\n"
        
        explanation += "\n⚠️  DISCLAIMER: This is an AI-assisted tool and should not\n"
        explanation += "   replace professional medical diagnosis.\n"
        
        return explanation


def predict_from_file(image_path, model_path=MODEL_PATH):
    """
    Convenience function to make a single prediction
    
    Args:
        image_path: Path to image file
        model_path: Path to trained model
    
    Returns:
        Prediction result dictionary
    """
    predictor = PneumoniaPredictor(model_path=model_path)
    return predictor.predict(image_path)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Pneumonia Classifier Inference')
    parser.add_argument('--image', type=str, required=True,
                       help='Path to chest X-ray image')
    parser.add_argument('--model', type=str, default=MODEL_PATH,
                       help='Path to trained model')
    parser.add_argument('--explain', action='store_true',
                       help='Show detailed explanation')
    
    args = parser.parse_args()
    
    # Check if image exists
    if not os.path.exists(args.image):
        print(f"Error: Image file '{args.image}' not found!")
        exit(1)
    
    # Check if model exists
    if not os.path.exists(args.model):
        print(f"Error: Model file '{args.model}' not found!")
        print("Please train the model first using train.py")
        exit(1)
    
    # Create predictor
    predictor = PneumoniaPredictor(model_path=args.model)
    
    # Make prediction
    print(f"\nAnalyzing image: {args.image}")
    print("="*60)
    
    if args.explain:
        explanation = predictor.explain_prediction(args.image)
        print(explanation)
    else:
        result = predictor.predict(args.image)
        print(f"\nPrediction: {result['predicted_label']}")
        print(f"Confidence: {result['confidence']*100:.2f}%")
        print("\nClass Probabilities:")
        for class_name, prob in result['probabilities'].items():
            print(f"  {class_name}: {prob*100:.2f}%")
