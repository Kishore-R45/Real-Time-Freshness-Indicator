# 1. Use Python 3.10 (TensorFlow compatible)
FROM python:3.10-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy requirements first (better caching)
COPY backend/requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy backend source code
COPY backend/ .

# 6. Expose port Render uses
EXPOSE 10000

# 7. Start Flask app with Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
