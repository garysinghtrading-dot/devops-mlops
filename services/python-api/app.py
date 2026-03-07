import os
import logging
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from functools import wraps
from google.cloud import storage

# 1. Setup Logging (Monitoring/Logging Requirement)
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("EvictionPredictionAPI")

app = Flask(__name__)

# Configuration
API_KEY = os.getenv("API_KEY", "dev-secret-key-123") # Will be injected via Kubernetes Secrets later
BUCKET_NAME = "machine-learning-416604-data-bucket"
MODEL_PATH = "models/eviction_v1/eviction_model_randomforest.joblib"
LOCAL_MODEL = "model.joblib"

# 2. Load Model on Startup
logger.info("Initializing service and downloading model from GCS...")
try:
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(MODEL_PATH)
    blob.download_to_filename(LOCAL_MODEL)
    model = joblib.load(LOCAL_MODEL)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

# 3. Authentication Decorator
def require_apikey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('x-api-key') == API_KEY:
            return view_function(*args, **kwargs)
        else:
            logger.warning("Failed authentication attempt.")
            return jsonify({"error": "Unauthorized. Invalid or missing API Key."}), 401
    return decorated_function

# 4. Health Check Route (Crucial for Kubernetes)
@app.route('/health', methods=['GET'])
def health_check():
    if model is None:
        return jsonify({"status": "unhealthy", "reason": "Model not loaded"}), 500
    return jsonify({"status": "healthy"}), 200

# 5. Prediction Route
@app.route('/predict', methods=['POST'])
@require_apikey
def predict():
    try:
        data = request.get_json()
        input_df = pd.DataFrame([data])
        
        # Make Prediction
        prediction_val = int(model.predict(input_df)[0])
        probability = float(model.predict_proba(input_df)[0][1])
        
        # Strict mapping to Class 0 and Class 1
        class_label = "Class 1" if prediction_val == 1 else "Class 0"
        
        response = {
            "prediction_class": class_label,
            "risk_probability": round(probability, 4)
        }
        
        # Log the prediction
        logger.info(f"Prediction made: {class_label} | Risk Prob: {response['risk_probability']} | Input data: {data}")
        
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Run on port 8080 for Cloud Run / GKE compatibility
    app.run(host='0.0.0.0', port=8080)