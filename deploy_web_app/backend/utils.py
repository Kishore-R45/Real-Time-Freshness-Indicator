import cv2
import numpy as np
import os

def preprocess_image(path):
    """
    Preprocess image for model prediction.
    - Reads image from disk
    - Converts BGR to RGB
    - Resizes to 224x224
    - Normalizes to [0, 1]
    - Adds batch dimension
    """

    if not os.path.exists(path):
        raise FileNotFoundError(f"Image file does not exist: {path}")

    img = cv2.imread(path)

    if img is None:
        raise ValueError(f"Failed to load image (cv2.imread returned None): {path}")

    # Convert BGR → RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize to model input size
    img = cv2.resize(img, (224, 224))

    # Normalize
    img = img.astype("float32") / 255.0

    # Add batch dimension
    img = np.expand_dims(img, axis=0)

    return img
