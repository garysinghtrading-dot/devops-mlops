# Real Estate Eviction Prediction Service  
**Jagpal Holdings – Microservice Architecture Documentation**

---

## 🏠 Overview

The **Real Estate Eviction Prediction Service** is a production-grade machine learning microservice deployed on **Google Kubernetes Engine (GKE)**. It provides real-time eviction risk scoring based on tenant financial and rental history characteristics.

This service powers the public-facing feature at: https://jagpalholdings.com/RealEstateEvictionServices


Users enter tenant information through a Razor Pages frontend, which sends a POST request to this microservice for inference.

---

## 🎯 Business Purpose

Jagpal Holdings Company historically faced financial losses due to tenant evictions.  
To mitigate this risk, a **Neural Network binary classifier** was trained on proprietary tenant history data to predict:

- **Stable tenancy**  
- **Potential eviction risk**

This microservice operationalizes that model in a scalable, cloud-native architecture.

---

## 🧩 High-Level Request Flow

```md
User → Razor Pages Frontend → GKE Cluster → Flask Microservice → GCS Model → Prediction Response
                          ┌──────────────────────────────────────────┐
                          │        User Browser (Frontend UI)        │
                          │  https://jagpalholdings.com/             │
                          │  /RealEstateEvictionServices             │
                          └──────────────────────────────────────────┘
                                           │
                                           │ 1. User enters:
                                           │    - MonthlyIncome
                                           │    - MonthlyDebt
                                           │    - EmploymentTenure
                                           │    - YearsAtPrevAddress
                                           │    - PrevEvictions
                                           │    - LatePaymentCount
                                           │    - CreditScore
                                           │    - ProposedRent
                                           │
                                           ▼
                     ┌──────────────────────────────────────────────┐
                     │      C#/.NET Razor Pages Frontend App        │
                     │  (Collects form data & sends POST request)   │
                     └──────────────────────────────────────────────┘
                                           │
                                           │ 2. POST /predict
                                           ▼
        ┌────────────────────────────────────────────────────────────────────┐
        │                     Google Kubernetes Engine (GKE)                 │
        │                                                                    │
        │   ┌────────────────────────────────────────────────────────────┐   │
        │   │                 Eviction Prediction Microservice            │   │
        │   │                     (Flask API Container)                   │   │
        │   │                                                            │   │
        │   │   Routes:                                                  │   │
        │   │     GET /        → Health check                            │   │
        │   │     POST /predict → Main inference endpoint                │   │
        │   │                                                            │   │
        │   │   Internal Logic:                                          │   │
        │   │     • Validate JSON payload                                │   │
        │   │     • Perform proprietary feature engineering              │   │
        │   │     • Call real_estate_services.make_real_estate_prediction│   │
        │   │                                                            │   │
        │   └────────────────────────────────────────────────────────────┘   │
        │                                                                    │
        └────────────────────────────────────────────────────────────────────┘
                                           │
                                           │ 3. Flask calls service layer
                                           ▼
                ┌────────────────────────────────────────────────────────┐
                │           real_estate_services.py (Service Layer)      │
                │                                                        │
                │   • Loads model ONCE using global variable             │
                │   • Prevents cold starts                               │
                │   • Orders features using private data_order list      │
                │   • Calls model.predict_proba()                        │
                │                                                        │
                └────────────────────────────────────────────────────────┘
                                           │
                                           │ 4. Model loaded from GCS (first call only)
                                           ▼
                     ┌──────────────────────────────────────────────┐
                     │      Google Cloud Storage (GCS Bucket)       │
                     │   • Stores trained eviction ML model         │
                     │   • Accessed via google-cloud-storage SDK    │
                     └──────────────────────────────────────────────┘
                                           │
                                           │ 5. Probability returned
                                           ▼
        ┌────────────────────────────────────────────────────────────────────┐
        │                     Flask Microservice Response                    │
        │                                                                    │
        │   Returns JSON:                                                    │
        │   {                                                                │
        │     "prediction": "<human-readable message>",                      │
        │     "score": <float probability>,                                  │
        │     "status": "success"                                            │
        │   }                                                                │
        └────────────────────────────────────────────────────────────────────┘
                                           │
                                           │ 6. Razor Pages displays result
                                           ▼
                          ┌──────────────────────────────────────────┐
                          │        User Sees Final Prediction        │
                          └──────────────────────────────────────────┘
