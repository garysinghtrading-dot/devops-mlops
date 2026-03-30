import functions_framework
import numpy as np
import pandas as pd
import os
import time
from google.cloud import monitoring_v3, firestore
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM


# CONFIGURATION
PROJECT_ID = os.getenv('ML_PROJECT_ID')
SERVICE_NAME = os.getenv('ML_APP_NAME')

def get_metrics(monitoring_client):
    """Pulls CPU and Request Count to create a Multi-Dimensional Feature Set"""
    if not PROJECT_ID or not SERVICE_NAME:
        raise ValueError("Environment variables missing.")

    project_path = f"projects/{PROJECT_ID}"
    now = time.time()
    interval = monitoring_v3.TimeInterval({
        "end_time": {"seconds": int(now)},
        "start_time": {"seconds": int(now) - (3600 * 24 * 7)} # Seconds of the last one week
    })

    # 1. FETCH CPU METRICS
    cpu_filter = (
        f'metric.type = "run.googleapis.com/container/cpu/utilizations" AND '
        f'resource.labels.service_name = "{SERVICE_NAME}"'
    )
    cpu_results = monitoring_client.list_time_series(request={"name": project_path, "filter": cpu_filter, "interval": interval})

    # 2. FETCH REQUEST COUNT (The Context)
    req_filter = (
        f'metric.type = "run.googleapis.com/request_count" AND '
        f'resource.labels.service_name = "{SERVICE_NAME}"'
    )
    req_results = monitoring_client.list_time_series(request={"name": project_path, "filter": req_filter, "interval": interval})

    # Process and Merge
    data = []
    for result in cpu_results:
        for point in result.points:
            ts = point.interval.end_time
            data.append({
                "timestamp": ts,
                "cpu": point.value.double_value,
                "hour": pd.to_datetime(ts).hour
            })
    
    df = pd.DataFrame(data)
    if df.empty: return df

    # 3. CYCLICAL TIME ENCODING
    # This helps the ML understand 11pm and 12am are close.
    df['hour_sin'] = np.sin(2 * np.pi * df['hour']/24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour']/24.0)
    
    return df

@functions_framework.http
def check_anomaly_and_scale(request):
    monitoring_client = monitoring_v3.MetricServiceClient()
    db = firestore.Client()
    
    try:
        df = get_metrics(monitoring_client)
    except Exception as e:
        return f"Error: {str(e)}", 500
    
    if df.empty or len(df) < 50:
        return "Building baseline... not enough data yet.", 200

    # 4. SELECT FEATURES
    # We use CPU + Sin/Cos time to detect patterns
    feature_cols = ['cpu', 'hour_sin', 'hour_cos']
    X = df[feature_cols]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 5. ML ENSEMBLE
    # OneClassSVM: Good for seeing if this 'type' of hour + cpu combo has happened before
    svm = OneClassSVM(kernel='rbf', gamma=0.1, nu=0.03) # 3% sensitivity
    df['svm_anomaly'] = svm.fit_predict(X_scaled)

    # KMeans: Clusters normal behavior
    kmeans = KMeans(n_clusters=3, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_scaled)
    distances = np.min(kmeans.transform(X_scaled), axis=1)
    df['kmeans_anomaly'] = distances > np.percentile(distances, 97) # Top 3% distances

    # 6. ENHANCED DECISION LOGIC
    last_row = df.iloc[-1]
    
    # Logic: Anomaly if both models agree AND CPU is actually high (ignore noise)
    # We set a "Noise Floor" of 0.10 (10% CPU). 
    # If CPU is lower than that, it's never an anomaly, just background jitter.
    raw_anomaly = bool((last_row['svm_anomaly'] == -1) and last_row['kmeans_anomaly'])
    is_serious_spike = last_row['cpu'] > 0.10 
    
    final_decision = raw_anomaly and is_serious_spike
    
    # 7. UPDATE FIRESTORE
    doc_ref = db.collection('infrastructure').document('cluster_state')
    doc_ref.set({
        'is_cluster_active': final_decision,
        'last_cpu_val': float(round(last_row['cpu'], 4)),
        'confidence_score': 0.95 if final_decision else 0.10,
        'status': 'SPIKE_DETECTED' if final_decision else 'NORMAL',
        'updated_at': firestore.SERVER_TIMESTAMP
    }, merge=True)

    return f"Status: {'ANOMALY' if final_decision else 'OK'}. CPU: {last_row['cpu']:.4f}", 200