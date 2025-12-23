import cv2
import numpy as np
from PIL import Image
import io

def preprocess_image_from_bytes(image_bytes):
    """
    Preprocess image from bytes for model prediction
    - Resize to 224x224
    - Normalize to 0-1 range
    - Add batch dimension
    """
    # Convert bytes to PIL Image
    image = Image.open(io.BytesIO(image_bytes))
    
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert to numpy array
    img = np.array(image)
    
    # Resize to model input size
    img = cv2.resize(img, (224, 224))
    
    # Normalize pixel values
    img = img.astype("float32") / 255.0
    
    # Add batch dimension
    img = np.expand_dims(img, axis=0)
    
    return img