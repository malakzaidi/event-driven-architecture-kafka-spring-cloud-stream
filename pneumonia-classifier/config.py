"""
Configuration file for Pneumonia Classifier
"""
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_DIR = os.path.join(BASE_DIR, 'models')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# Model Configuration
MODEL_NAME = 'pneumonia_classifier.pth'
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)
NUM_CLASSES = 2  # Normal, Pneumonia
IMAGE_SIZE = 224
BATCH_SIZE = 32
NUM_EPOCHS = 10
LEARNING_RATE = 0.001

# Class names
CLASS_NAMES = ['Normal', 'Pneumonia']

# Training Configuration
TRAIN_SPLIT = 0.8
VAL_SPLIT = 0.1
TEST_SPLIT = 0.1
RANDOM_SEED = 42

# Data Augmentation
AUGMENTATION = {
    'rotation_range': 15,
    'width_shift_range': 0.1,
    'height_shift_range': 0.1,
    'horizontal_flip': True,
    'zoom_range': 0.1
}

# Device Configuration
DEVICE = 'cuda'  # Will fallback to 'cpu' if CUDA not available

# Flask Configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = False
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
