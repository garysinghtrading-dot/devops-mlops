import os
import logging
from flask import Flask, request, jsonify 
import pandas as pd 
import real_estate_services

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
def status():
    """Service availability endpoint."""
    return "Eviction Prediction API - Status: Operational"

@app.route('/predict', methods=['POST'])
def predict_real_estate_eviction():
    """
    Public API endpoint for tenant risk analysis.
    Returns a probability score based on proprietary inference logic.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            "prediction": "No input data provided", 
            "score": -1.0,
            "status": "error"
        }), 400

    try:
        logging.info("Analyzing request via service layer...")
        
        # Internal processing and feature engineering abstracted to private module (hidden from public view)
        # Specific model weights and parameters are managed in a private module
        # data_order is abstracted in a private module
        data_order = [feature1, feature2, 
            feature3, feature4, feature5, feature6, 
            feature7, feature8, feature9, feature10, 
            feature11, feature12, feature13, feature14
        ] # All inputs are abstracted to protect intellectual property
        score = real_estate_services.make_real_estate_prediction(data, data_order)

        if score >= 0.5:
            msg = f"Analysis suggests a {score * 100:.2f}% probability of successful tenancy."
        else:
            msg = f"Analysis suggests a {(1 - score) * 100:.2f}% probability of potential eviction risk."

        return jsonify({
            "prediction": msg, 
            "score": float(score),
            "status": "success"
        })

    except Exception as e:
        logging.error(f"Inference error: {str(e)}")
        return jsonify({
            "prediction": "Internal processing error",
            "score": 0.0,
            "status": "error"
        }), 500

if __name__ == "__main__":
    # Environment-aware port configuration for Cloud Run/GKE
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)