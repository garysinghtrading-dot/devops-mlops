FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app.py . 

# Expose port 8080 (matching your app.py)
EXPOSE 8080

# Use gunicorn for production-grade serving
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]