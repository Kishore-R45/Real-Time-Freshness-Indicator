from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import numpy as np
from datetime import date
from tensorflow.keras.models import load_model
from utils import preprocess_image
from decay import compute_all_decay, IDEAL_SHELF, ROOM_SHELF, HIGH_HUMIDITY_SHELF

app = Flask(__name__)
CORS(app,
     resources={r"/api/*": {"origins": [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://freshness-indicator.netlify.app/"
    ]}},
    supports_credentials=True
)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Create uploads folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model once at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model.h5')
model = load_model(MODEL_PATH)

# Supported fruits and vegetables
SUPPORTED_ITEMS = [
    {"value": "apple", "label": "Apple"},
    {"value": "banana", "label": "Banana"},
    {"value": "tomato", "label": "Tomato"},
    {"value": "orange", "label": "Orange"},
    {"value": "potato", "label": "Potato"},
    {"value": "cucumber", "label": "Cucumber"},
    {"value": "capsicum", "label": "Capsicum"},
    {"value": "okra", "label": "Okra"}
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Freshness API is running"})

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({"items": SUPPORTED_ITEMS})

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400
        
        file = request.files['image']
        fruit = request.form.get('fruit', '').lower()
        
        # Validate file
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type. Allowed: png, jpg, jpeg, webp"}), 400
        
        # Validate fruit
        if fruit not in IDEAL_SHELF:
            return jsonify({"error": f"Unsupported item: {fruit}"}), 400
        
        # Save and process file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Preprocess and predict
            img = preprocess_image(filepath)
            initial_freshness = float(model.predict(img, verbose=0)[0][0])
            initial_freshness = max(0, min(round(initial_freshness, 2), 100))
            
            # Compute decay
            decay_data = compute_all_decay(initial_freshness, fruit, date.today())
            
            # Determine status
            room_final = decay_data['room_final']
            if room_final > 70:
                status = "FRESH"
                status_color = "#22c55e"  # green
            elif room_final > 40:
                status = "CONSUME SOON"
                status_color = "#f59e0b"  # amber
            else:
                status = "SPOILED"
                status_color = "#ef4444"  # red
            
            # Prepare response
            response = {
                "success": True,
                "fruit": fruit.capitalize(),
                "initial_freshness": initial_freshness,
                "decay": decay_data,
                "status": status,
                "status_color": status_color,
                "shelf_life": {
                    "ideal": IDEAL_SHELF[fruit],
                    "room": ROOM_SHELF[fruit],
                    "humid": HIGH_HUMIDITY_SHELF[fruit]
                },
                "chart_data": {
                    "labels": ["Ideal Storage", "Room Temp", "High Humidity"],
                    "freshness": [
                        decay_data['ideal_final'],
                        decay_data['room_final'],
                        decay_data['humid_final']
                    ],
                    "days_left": [
                        decay_data['ideal_days_left'],
                        decay_data['room_days_left'],
                        decay_data['humid_days_left']
                    ]
                }
            }
            
            return jsonify(response)
            
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
                
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/shelf-life/<fruit>', methods=['GET'])
def get_shelf_life(fruit):
    fruit = fruit.lower()
    if fruit not in IDEAL_SHELF:
        return jsonify({"error": "Unsupported item"}), 400
    
    return jsonify({
        "fruit": fruit,
        "ideal": IDEAL_SHELF[fruit],
        "room": ROOM_SHELF[fruit],
        "humid": HIGH_HUMIDITY_SHELF[fruit]
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)