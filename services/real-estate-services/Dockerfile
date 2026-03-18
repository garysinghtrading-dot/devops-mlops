FROM python:3.11-slim

# 1. Install system-level dependencies (CRITICAL for scikit-learn/pandas)
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 2. Set environment variables
ENV PYTHONUNBUFFERED=True
ENV APP_HOME=/app
WORKDIR $APP_HOME

# 3. Install Python dependencies from your file
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy local code
COPY . .

# 5. Start the server
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app