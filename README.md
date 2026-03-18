# Jagpal Holdings – Cloud Infrastructure & Microservices

This repository contains the production-grade cloud infrastructure and microservices powering **Jagpal Holdings Company**, deployed on **Google Cloud Platform** using **Kubernetes (GKE)** and **Terraform**.

---

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

For detailed diagrams, see:  
📄 `docs/architecture/high-level-architecture.md`

---

## 🧩 Microservices

| Service | Description | Docs |
|--------|-------------|------|
| Eviction Prediction | ML-powered tenant risk scoring | `docs/services/eviction-service.md` |
| Stock Data Service | Proxy for financial market data | `docs/services/stock-data-service.md` |
| Login Service | Authentication microservice | `docs/services/login-service.md` |

---

## 🛠️ Infrastructure

- Google Kubernetes Engine (GKE)
- Terraform IaC
- Artifact Registry
- Cloud Storage (Model Hosting)
- Internal Networking (ClusterIP)

Full infra docs:  
📄 `docs/infrastructure/terraform-layout.md`

---

## 📦 Deployment

See:  
📄 `docs/operations/deployment-guide.md`

---

## 👨‍💻 Author  
Developed by **Gurpreet Jagpal** – Jagpal Holdings Company
