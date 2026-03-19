# 🛠️ System Monitoring & Health Architecture

This document outlines the automated anomaly detection and scaling lifecycle for our containerized applications hosted on **Google Cloud Platform (GCP)**.

---

## 📡 Data Collection Layer
We monitor application health and resource utilization through a decoupled, serverless approach:

* **Trigger:** A **Cloud Scheduler** cron job fires every 10 minutes.
* **Ingestion:** Hits a **Cloud Run Function** via HTTP URL.
* **Metrics:** The function queries the **GCP Monitoring API** to pull:
    * `CPU Usage` 🖥️
    * `Memory Utilization` 🧠
    * `Request Latency / Health Status` 🏥

---

## 🤖 Anomaly Detection Logic (ML Layer)
To prevent false positives, we utilize a dual-model ensemble approach. An anomaly is only confirmed if **both** models agree.

### 1. KMeans Clustering 📍
* **Logic:** Measures the Euclidean distance of the latest data point to its assigned cluster centroid.
* **Threshold:** If the distance is in the **top 5%** of historical distances, it is flagged as an anomaly.

### 2. One-Class SVM 🛡️
* **Logic:** A non-linear outlier detection algorithm.
* **Threshold:** If the model predicts a value of `-1`, the data point is considered an outlier.

> ⚠️ **Decision Gate:** Scaling logic only proceeds if `(KMeans == Anomaly) AND (OneClassSVM == -1)`.

---

## 🚀 Scaling & Failover Orchestration
Once an anomaly is confirmed, the system checks the current infrastructure state before taking action.

### 🚩 State Management (Firestore)
We use **Cloud Firestore** as a global state coordinator.
* **Document:** `system/status`
* **Field:** `status` (String) | `cluster_ip` (String)

### ⚙️ The Scaling Workflow
1.  **Check Status:** The system reads the `status` flag in Firestore.
2.  **Trigger Infrastructure:** If `status != 'NORMAL'`, the Cloud Function triggers **Terraform** to spin up a new compute cluster.
3.  **Update Registry:** Once the cluster is live, its **IP Address** is written to Firestore.

---

## 🔄 Backend Routing Logic
Our backend container applications perform a lookup to Firestore to determine where to route traffic:

| Cluster Active? | Routing Destination |
| :--- | :--- |
| **NO** | Default Backend Container URL 🔗 |
| **YES** | Cluster IP Address (Scaled Infrastructure) 🌐 |

---

## 📈 Maintenance & Troubleshooting
* **Model Retraining:** The `OneClassSVM` and `KMeans` models are refit during the execution of the Cloud Function to ensure they adapt to evolving traffic patterns.
* **Manual Override:** To stop the scaling logic manually, update the Firestore `status` flag to `NORMAL`.

---
*Last Updated: March 2026*