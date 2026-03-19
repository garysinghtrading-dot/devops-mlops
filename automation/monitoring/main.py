import functions_framework
import pandas as pd
import numpy as np
import time
import os
from google.cloud import monitoring_v3, firestore
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
from sklearn.cluster import KMeans

# ==========================================
# 1. CONFIGURATION (Environment Variables)
# ==========================================
# We pull these from the Cloud Function environment settings
PROJECT_ID = os.getenv('ML_PROJECT_ID') # FROM secrets.env FILE - NOT COMMITED TO REPO
SERVICE_NAME = os.getenv('ML_APP_NAME') # FROM secrets.env FILE - NOT COMMITED TO REPO

def get_metrics(monitoring_client):
    """Pulls 7 days of CPU utilization for the specific service"""
    if not PROJECT_ID or not SERVICE_NAME:
        raise ValueError("Environment variables ML_PROJECT_ID or ML_APP_NAME are missing.")

    now = time.time()
    seconds = int(now)
    project_path = f"projects/{PROJECT_ID}"
    
    interval = monitoring_v3.TimeInterval({
        "end_time": {"seconds": seconds},
        "start_time": {"seconds": seconds - (3600 * 24 * 7)} # LAST 7 DAYS OF DATA
    })

    filter_str = (
        f'metric.type = "run.googleapis.com/container/cpu/utilizations" AND '
        f'resource.type = "cloud_run_revision" AND '
        f'resource.labels.service_name = "{SERVICE_NAME}"'
    )

    results = monitoring_client.list_time_series(
        request={"name": project_path, "filter": filter_str, "interval": interval}
    )
    
    data = []
    for result in results:
        for point in result.points:
            ts = point.interval.end_time
            data.append({
                "timestamp": ts,
                "cpu_utilization": point.value.double_value,
                "hour": pd.to_datetime(ts).hour,
                "day_of_week": pd.to_datetime(ts).dayofweek
            })
    return pd.DataFrame(data)

@functions_framework.http
def check_anomaly_and_scale(request):
    """The main entry point for the Cloud Function"""
    
    # Initialize clients inside the handler (best for security/portability)
    monitoring_client = monitoring_v3.MetricServiceClient()
    db = firestore.Client()
    
    # 1. Data Retrieval
    try:
        df = get_metrics(monitoring_client)
    except Exception as e:
        return f"Error fetching metrics: {str(e)}", 500
    
    if df.empty or len(df) < 50:
        return "Insufficient data for analysis. Need at least 50 historical points.", 200

    # 2. Feature Engineering & Scaling
    features = df[['cpu_utilization', 'hour', 'day_of_week']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    # 3. ML Model 1: OneClassSVM (Boundary Detection)
    # nu=0.05 targets a 5% outlier rate
    svm = OneClassSVM(kernel='rbf', gamma=0.1, nu=0.05)
    df['svm_anomaly'] = svm.fit_predict(X_scaled)

    # 4. ML Model 2: KMeans (Distance Outlier Detection)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_scaled)
    distances = np.min(kmeans.transform(X_scaled), axis=1)
    threshold = np.percentile(distances, 95)
    df['kmeans_anomaly'] = distances > threshold

    # 5. Consensus Logic
    last_row = df.iloc[-1]
    
    # Explicit conversion from NumPy to Python types for Firestore compatibility
    is_anomaly = bool((last_row['svm_anomaly'] == -1) and last_row['kmeans_anomaly'])
    cpu_val = float(last_row['cpu_utilization'])
    
    # 6. Action: Update Firestore 'Switch'
    doc_ref = db.collection('infrastructure').document('cluster_state')
    
    doc_ref.set({
        'is_cluster_active': is_anomaly,
        'last_cpu_val': round(cpu_val, 4),
        'status': 'ANOMALY_DETECTED' if is_anomaly else 'NORMAL',
        'updated_at': firestore.SERVER_TIMESTAMP
    }, merge=True)

    status_msg = f"Analysis complete. Anomaly Detected: {is_anomaly}. Firestore Updated."
    print(status_msg) 
    
    return status_msg, 200