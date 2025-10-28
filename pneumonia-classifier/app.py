"""
Flask API for Pneumonia Classifier
Provides REST endpoints for image upload and prediction
"""
import os
import io
import base64
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PIL import Image
import torch

from predict import PneumoniaPredictor
from config import *

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize predictor
predictor = None


def allowed_file(filename):
    """
    Check if file extension is allowed
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def init_predictor():
    """
    Initialize the predictor (lazy loading)
    """
    global predictor
    if predictor is None:
        if os.path.exists(MODEL_PATH):
            predictor = PneumoniaPredictor(model_path=MODEL_PATH)
            print("✅ Model loaded successfully!")
        else:
            print("⚠️  Warning: Model not found. Please train the model first.")
            print(f"Expected model path: {MODEL_PATH}")


@app.route('/')
def index():
    """
    Serve the main page
    """
    return send_from_directory('static', 'index.html')


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    model_loaded = predictor is not None
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded,
        'device': str(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Prediction endpoint
    Accepts image file upload and returns prediction
    """
    # Initialize predictor if not already done
    if predictor is None:
        init_predictor()
        if predictor is None:
            return jsonify({
                'error': 'Model not loaded. Please train the model first.'
            }), 500
    
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if file is allowed
    if not allowed_file(file.filename):
        return jsonify({
            'error': f'Invalid file type. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
        }), 400
    
    try:
        # Read image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Make prediction
        result = predictor.predict(image, return_probabilities=True)
        
        # Add additional info
        result['success'] = True
        result['filename'] = secure_filename(file.filename)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500


@app.route('/api/predict_base64', methods=['POST'])
def predict_base64():
    """
    Prediction endpoint for base64 encoded images
    """
    # Initialize predictor if not already done
    if predictor is None:
        init_predictor()
        if predictor is None:
            return jsonify({
                'error': 'Model not loaded. Please train the model first.'
            }), 500
    
    # Get JSON data
    data = request.get_json()
    
    if not data or 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400
    
    try:
        # Decode base64 image
        image_data = data['image']
        
        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Make prediction
        result = predictor.predict(image, return_probabilities=True)
        
        # Add additional info
        result['success'] = True
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500


@app.route('/api/batch_predict', methods=['POST'])
def batch_predict():
    """
    Batch prediction endpoint
    Accepts multiple image files
    """
    # Initialize predictor if not already done
    if predictor is None:
        init_predictor()
        if predictor is None:
            return jsonify({
                'error': 'Model not loaded. Please train the model first.'
            }), 500
    
    # Check if files are present
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    
    if len(files) == 0:
        return jsonify({'error': 'No files selected'}), 400
    
    results = []
    
    for file in files:
        if file and allowed_file(file.filename):
            try:
                # Read image
                image_bytes = file.read()
                image = Image.open(io.BytesIO(image_bytes))
                
                # Make prediction
                result = predictor.predict(image, return_probabilities=True)
                result['filename'] = secure_filename(file.filename)
                result['success'] = True
                
                results.append(result)
            
            except Exception as e:
                results.append({
                    'filename': secure_filename(file.filename),
                    'success': False,
                    'error': str(e)
                })
    
    return jsonify({
        'results': results,
        'total': len(results),
        'successful': sum(1 for r in results if r.get('success', False))
    })


@app.route('/api/model_info', methods=['GET'])
def model_info():
    """
    Get model information
    """
    if predictor is None:
        init_predictor()
    
    if predictor is None or predictor.model is None:
        return jsonify({
            'error': 'Model not loaded'
        }), 404
    
    # Count parameters
    total_params = sum(p.numel() for p in predictor.model.parameters())
    trainable_params = sum(p.numel() for p in predictor.model.parameters() if p.requires_grad)
    
    return jsonify({
        'model_type': 'ResNet18 (Transfer Learning)',
        'num_classes': NUM_CLASSES,
        'class_names': CLASS_NAMES,
        'image_size': IMAGE_SIZE,
        'total_parameters': total_params,
        'trainable_parameters': trainable_params,
        'device': str(predictor.device)
    })


@app.errorhandler(413)
def request_entity_too_large(error):
    """
    Handle file too large error
    """
    return jsonify({
        'error': f'File too large. Maximum size: {MAX_CONTENT_LENGTH / (1024*1024):.0f}MB'
    }), 413


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors
    """
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors
    """
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Initialize predictor on startup
    print("="*60)
    print("🚀 Starting Pneumonia Classifier API")
    print("="*60)
    
    init_predictor()
    
    print(f"\n📍 Server will run on http://{FLASK_HOST}:{FLASK_PORT}")
    print(f"📊 Frontend available at http://localhost:{FLASK_PORT}")
    print("\n⚠️  Note: This is a development server. Use a production WSGI server for deployment.")
    print("="*60 + "\n")
    
    # Run Flask app
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=FLASK_DEBUG
    )
