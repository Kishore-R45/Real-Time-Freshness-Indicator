import cv2
import numpy as np

def preprocess_image(path):
    """
    Preprocess image for model prediction
    - Resize to 224x224
    - Normalize to 0-1 range
    - Add batch dimension
    """
    img = cv2.imread(path)
    
    if img is None:
        raise ValueError(f"Image not found or could not be loaded: {path}")
    
    # Convert BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Resize to model input size
    img = cv2.resize(img, (224, 224))
    
    # Normalize pixel values
    img = img.astype("float32") / 255.0
    
    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    
    return img