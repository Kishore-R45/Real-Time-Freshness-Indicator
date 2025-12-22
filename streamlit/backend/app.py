from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import base64
from predict_api import predict_freshness

app = Flask(__name__)
CORS(app)

# Supported fruits and vegetables
SUPPORTED_ITEMS = [
    "Apple", "Banana", "Tomato", "Orange", 
    "Potato", "Cucumber", "Capsicum", "Okra"
]

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "API is running"})

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify({"items": SUPPORTED_ITEMS})

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        if 'image' not in request.files and 'image_base64' not in request.json:
            return jsonify({"error": "No image provided"}), 400
        
        fruit = request.form.get('fruit') or request.json.get('fruit')
        if not fruit:
            return jsonify({"error": "No fruit/vegetable type provided"}), 400
        
        # Handle file upload
        if 'image' in request.files:
            image_file = request.files['image']
            # Save temporarily
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, "uploaded_image.jpg")
            image_file.save(temp_path)
        else:
            # Handle base64 image
            image_base64 = request.json.get('image_base64')
            image_data = base64.b64decode(image_base64.split(',')[1] if ',' in image_base64 else image_base64)
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, "uploaded_image.jpg")
            with open(temp_path, 'wb') as f:
                f.write(image_data)
        
        # Get prediction
        result = predict_freshness(temp_path, fruit.lower())
        
        # Cleanup
        os.remove(temp_path)
        os.rmdir(temp_dir)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/predict/base64', methods=['POST'])
def predict_base64():
    try:
        data = request.json
        
        if 'image' not in data:
            return jsonify({"error": "No image provided"}), 400
        
        fruit = data.get('fruit')
        if not fruit:
            return jsonify({"error": "No fruit/vegetable type provided"}), 400
        
        # Decode base64 image
        image_base64 = data['image']
        if ',' in image_base64:
            image_data = base64.b64decode(image_base64.split(',')[1])
        else:
            image_data = base64.b64decode(image_base64)
        
        # Save temporarily
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, "uploaded_image.jpg")
        with open(temp_path, 'wb') as f:
            f.write(image_data)
        
        # Get prediction
        result = predict_freshness(temp_path, fruit.lower())
        
        # Cleanup
        os.remove(temp_path)
        os.rmdir(temp_dir)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)