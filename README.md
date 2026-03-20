# 🏢 **Jagpal Holdings – Cloud Infrastructure & Microservices**

This repository contains the **production‑grade cloud infrastructure and microservices** that power Jagpal Holdings Company.  
The platform is deployed on **Google Cloud Platform (GCP)** using:

- **Google Kubernetes Engine (GKE)**
- **Terraform (Infrastructure as Code)**
- **Dockerized microservices**
- **Internal service‑to‑service networking**

This repository focuses on **scalable cloud architecture**, not machine learning pipelines.  
Its purpose is to demonstrate how Jagpal Holdings deploys, scales, and operates its services in a modern cloud‑native environment.

---

# 🚀 **High‑Level Architecture**



## 🚀 High-Level Architecture
[ User Browser ] 
       |
       ▼
[ jagpalholdings.com (C# Frontend) ] --- (Public Internet) ---┐
       |                                                     |
       | (Internal Cluster Networking)                       |
       ▼                                                     ▼
[ GKE Ingress / Load Balancer ] <----------------------------┘
       |
       ├──▶ [ Eviction Service (Python/MLP) ] ---▶ [ GCS (Model) ]
       ├──▶ [ Stock Data Service (Python) ]
       └──▶ [ Login Service (Auth) ]


Each microservice is deployed as an independent container, scaled and managed by Kubernetes, and exposed internally via ClusterIP services.  
Only the frontend is publicly accessible.

---

# 🧩 **Microservices Overview**

## **1. Real Estate Eviction Service**
Backend for:  
https://jagpalholdings.com/RealEstateEvictionServices

This service receives tenant financial and rental history via HTTP POST and runs a **binary classifier** trained on Jagpal Holdings’ proprietary tenant dataset.  
It returns a probability score indicating **eviction risk**.

**Highlights:**
- Python Flask microservice  
- Model loaded from GCS at startup  
- Stateless inference endpoint  
- Integrated with C# frontend  
- Deployed on GKE  

Detailed architecture:  
`docs/architecture/real-estate-services.md`

---

## **2. Stock Data Service (Coming Soon)**
A microservice designed to help traders understand:

- how anomalous a stock move is  
- whether a price movement is an outlier  
- whether mean reversion is likely  

Jagpal Holdings actively trades securities, and this service exposes some of the quantitative insights used internally.
Detailed architecture:  
`docs/architecture/stock-data-services.md`
---

## **3. Login Service (Coming Soon)**
A secure authentication microservice that:

- accepts username/password  
- validates credentials against **Azure SQL Database**  
- uses salted + hashed passwords  
- returns authentication results to the frontend  

This service is **internal‑only** (ClusterIP) and not exposed to the public internet.

## ✅ Current State

The system is actively under development. The following components are fully implemented and working:

- Infrastructure as Code (Terraform) provisions a cluster and deploys services
- Microservice architecture is established and operational
- Real Estate Eviction Service backend is implemented
  - Loads a trained `.joblib` model
  - Performs prediction on eviction risk
  - Exposes results through a service endpoint

Additional microservices and workflows are being added incrementally.
---

# 🏛️ **About Jagpal Holdings Company**

**Websites:**  
- https://jagpalholdings.com  
- https://www.accountplusfinance.com  

Jagpal Holdings Company is a real estate and securities holdings firm.  
The company is expanding into **data‑driven services**, leveraging internal datasets to build predictive tools that reduce operational risk and improve decision‑making.

### Example:
Tenant evictions were a major overhead cost.  
By analyzing historical tenant data, Gurpreet Jagpal built a proprietary eviction‑risk model that now powers the Real Estate Eviction Service.

---

# 🔮 **Future Services**

### **1. Stock Data Analytics API**
Statistical anomaly detection for traders, based on the same quantitative models used internally by Jagpal Holdings.

### **2. Portfolio Management Chatbot**
An AI‑powered assistant integrated directly into jagpalholdings.com, allowing traders to ask questions about their holdings and receive data‑driven insights.

---

# 👨‍💻 **Developed by**  
**Gurpreet Singh Jagpal**  
Founder, Jagpal Holdings Company

