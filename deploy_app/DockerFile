# ================================
# Base image: Python 3.10 (TensorFlow compatible)
# ================================
FROM python:3.10-slim

# ================================
# Set working directory
# ================================
WORKDIR /app

# ================================
# Install system-level dependencies
# Required for OpenCV (cv2) and image processing
# ================================
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ================================
# Copy project files into container
# ================================
COPY . .

# ================================
# Upgrade pip
# ================================
RUN pip install --no-cache-dir --upgrade pip

# ================================
# Install Python dependencies
# ================================
RUN pip install --no-cache-dir -r requirements.txt

# ================================
# Expose Streamlit default port
# ================================
EXPOSE 8501

# ================================
# Run Streamlit app (entry point)
# ================================
CMD ["streamlit", "run", "streamlit/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
