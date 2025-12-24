# =========================
# 1️⃣ Build React frontend
# =========================
FROM node:18 AS frontend-build

WORKDIR /frontend

# Install frontend dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy frontend source
COPY frontend/ .
RUN npm run build


# =========================
# 2️⃣ Flask + ML backend
# =========================
FROM python:3.10-slim

WORKDIR /app

# System dependencies (required for OpenCV)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy backend code
COPY backend /app/backend

# Copy React build output into Flask static folder
# (Vite output is "dist")
COPY --from=frontend-build /frontend/dist /app/backend/static

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/backend/requirements.txt

# Hugging Face uses port 7860
EXPOSE 7860

# Run Flask as a module (IMPORTANT)
CMD ["python", "-m", "backend.app"]
