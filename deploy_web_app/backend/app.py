from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from datetime import date
from tensorflow.keras.models import load_model

# ✅ Package-based imports (Docker safe)
from backend.utils import preprocess_image
from backend.decay import (
    compute_all_decay,
    IDEAL_SHELF,
    ROOM_SHELF,
    HIGH_HUMIDITY_SHELF
)

# --------------------------------
# Flask App Configuration
# --------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    static_url_path=""
)

# Same-origin (React + Flask in same container)
CORS(app)

# --------------------------------
# Upload configuration
# --------------------------------
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --------------------------------
# Load model ONCE (cold start)
# --------------------------------
MODEL_PATH = os.path.join(BASE_DIR, "model.h5")
model = load_model(MODEL_PATH)

# --------------------------------
# Supported items
# --------------------------------
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
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# --------------------------------
# API ROUTES
# --------------------------------
@app.route("/api/health")
def health_check():
    return jsonify({"status": "healthy"})

@app.route("/api/items")
def get_items():
    return jsonify({"items": SUPPORTED_ITEMS})

@app.route("/api/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image file"}), 400

    file = request.files["image"]
    fruit = request.form.get("fruit", "").lower()

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    if fruit not in IDEAL_SHELF:
        return jsonify({"error": "Unsupported item"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        img = preprocess_image(filepath)
        initial = float(model.predict(img, verbose=0)[0][0])
        initial = max(0, min(round(initial, 2), 100))

        decay = compute_all_decay(initial, fruit, date.today())

        room_final = decay["room_final"]
        if room_final > 70:
            status = "FRESH"
            color = "#22c55e"
        elif room_final > 40:
            status = "CONSUME SOON"
            color = "#f59e0b"
        else:
            status = "SPOILED"
            color = "#ef4444"

        return jsonify({
            "success": True,
            "fruit": fruit.capitalize(),
            "initial_freshness": initial,
            "decay": decay,
            "status": status,
            "status_color": color
        })

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

# --------------------------------
# Serve React (Vite build)
# --------------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)

    index_path = os.path.join(app.static_folder, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(app.static_folder, "index.html")

    return jsonify({"error": "Frontend build not found"}), 404

# --------------------------------
# Hugging Face entry point
# --------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
