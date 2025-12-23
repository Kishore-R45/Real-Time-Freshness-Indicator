from tensorflow.keras.models import load_model
from utils import preprocess_image
from decay import compute_all_decay
from datetime import date
import os

# Load model once
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.h5")
model = None

def get_model():
    global model
    if model is None:
        model = load_model(MODEL_PATH)
    return model

def predict_freshness(image_path, fruit):
    """
    Predict freshness of fruit/vegetable from image
    Returns comprehensive freshness report
    """
    model = get_model()
    
    # Preprocess image
    img = preprocess_image(image_path)
    
    # Predict initial freshness
    initial = model.predict(img, verbose=0)[0][0]
    initial = max(0, min(round(float(initial), 2), 100))
    
    # Compute decay for all conditions
    decay = compute_all_decay(initial, fruit.lower(), date.today())
    
    # Determine status based on room freshness
    room_freshness = decay['room_final']
    
    if room_freshness > 70:
        status = "FRESH"
        status_color = "#22c55e"  # Green
        status_icon = "✅"
        recommendation = "Safe to consume. Store properly to maintain freshness."
    elif room_freshness > 40:
        status = "CONSUME SOON"
        status_color = "#f59e0b"  # Orange/Amber
        status_icon = "⚠️"
        recommendation = "Quality is declining. Consume within the next day or two."
    else:
        status = "SPOILED"
        status_color = "#ef4444"  # Red
        status_icon = "❌"
        recommendation = "Not recommended for consumption. Please discard."
    
    # Build comprehensive result
    result = {
        "success": True,
        "fruit": fruit.capitalize(),
        "initial_freshness": initial,
        
        # Freshness by storage condition
        "conditions": {
            "ideal": {
                "name": "Ideal Storage",
                "description": "Refrigerated at optimal temperature",
                "freshness": decay['ideal_final'],
                "days_left": decay['ideal_days_left'],
                "icon": "❄️"
            },
            "room": {
                "name": "Room Temperature",
                "description": "Normal room conditions (~25°C)",
                "freshness": decay['room_final'],
                "days_left": decay['room_days_left'],
                "icon": "🏠"
            },
            "humid": {
                "name": "High Humidity",
                "description": "Humid environment (>80% RH)",
                "freshness": decay['humid_final'],
                "days_left": decay['humid_days_left'],
                "icon": "💧"
            }
        },
        
        # Overall status
        "status": status,
        "status_color": status_color,
        "status_icon": status_icon,
        "recommendation": recommendation,
        
        # Chart data
        "chart_data": {
            "labels": ["Ideal Storage", "Room Temp", "High Humidity"],
            "freshness_values": [
                decay['ideal_final'],
                decay['room_final'],
                decay['humid_final']
            ],
            "days_left": [
                decay['ideal_days_left'],
                decay['room_days_left'],
                decay['humid_days_left']
            ]
        },
        
        # Additional metadata
        "days_since_upload": decay['days_passed'],
        "analysis_date": str(date.today())
    }
    
    return result