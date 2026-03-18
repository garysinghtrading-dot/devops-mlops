from google.cloud import storage
import joblib
import io
import sys
import os

# Environment variables
BUCKET_NAME = os.getenv("BUCKET_NAME")
MODEL_PATH = os.getenv("MODEL_PATH")

model = None 

# Load once at the module level (Global)
def _load_model_once():
    global model  # Declare global FIRST
    if model is None:
        print("Model is None, starting GCS download...")
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(MODEL_PATH)
        buffer = io.BytesIO()
        blob.download_to_file(buffer)
        buffer.seek(0)
        model = joblib.load(buffer)
        print("Model loaded successfully into global memory.")
    return model


def make_real_estate_prediction(data, data_order):
    # Fix the typo and extract the first result [0] and the "Not Evicted" prob [0]
    # This runs once when the service is imported
    rf_model = _load_model_once()
    probabilities = rf_model.predict_proba(data[data_order])
    return probabilities[0][0] # Returns the float for Class 0