from google.cloud import storage
import joblib
import io
import sys
import os

# Environment variables
BUCKET_NAME = os.getenv("BUCKET_NAME") # GCS Bucket Name
MODEL_PATH = os.getenv("MODEL_PATH") # Path to the model in GCS storage

model = None 

'''
    METHOD _load_model_once
    * Used to load in model once 
    * Once loaded in, prevents cold starts in the future
'''
# Load once at the module level (Global)
def _load_model_once():
    global model  # Declare global FIRST, precents cold starts in the future
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

'''
    * METHOD: make_real_estate_prediction
    * ARGS:
        * data -> pandas dataframe that holds the input data for prediction
        * data_order -> python list for the order of features for input 
    RETURNS:
        * Returns a prediction probability of real estate eviction
'''
def make_real_estate_prediction(data, data_order):
    # Load Model
    rf_model = _load_model_once()
    probabilities = rf_model.predict_proba(data[data_order])
    return probabilities[0][0] # Returns the float for Class 0