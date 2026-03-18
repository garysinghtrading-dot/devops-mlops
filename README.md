# DevOps & MLOps: Scaling Jagpal Holdings

## Project Overview
This repository manages the high-scale backend infrastructure for **jagpalholdings.com**, a production container application running on Google Cloud Platform. 

The primary goal of this project is to demonstrate the transition from a standalone application to a distributed, containerized architecture using **Kubernetes (GKE)** and **Infrastructure as Code (Terraform)**. While the core business logic serves Jagpal Holdings Company, this repo focuses on the **Reliability, Scalability, and Deployment** of those services.

---

## 🏗️ Featured Service: Real Estate Eviction Prediction
**URL:** `jagpalholdings.com/RealEstateEvictionServices`

### The Business Case
Born from the operational needs of **Jagpal Holdings Company**, this service addresses the financial risk of tenant evictions. By analyzing historical data—including credit scores, monthly income, and proposed rent—I developed a **Neural Network binary classifier** to identify high-risk eviction profiles based on our company's specific tenant history.

### Technical Implementation & "Shift Left" Logic
* **Interface:** The service accepts `POST` HTTP requests containing tenant characteristics from the frontend.
* **Feature Engineering:** Upon receiving a request, the backend performs proprietary feature engineering. Specific inputs and newly engineered transformations are kept private to protect Intellectual Property.
* **Performance Optimization (Cold Start Mitigation):** * To combat "cold start" latency common in containerized environments, the `real_estate_services` module loads the Neural Network model and stores it in a **global variable** upon initialization.
    * This ensures that subsequent requests find the model already in memory, providing near-instant inference.
* **Prediction Logic:** The system evaluates the model's output probability. 
    * If the predicted probability is $\ge 0.5$, it flags a high eviction risk.
    * If the probability is $< 0.5$, it confirms a stable profile.
* **Response:** Results are returned as a clean JSON payload for seamless integration with the C#/.NET frontend.

---

## 🛠️ Infrastructure & DevOps Stack
While the Data Science pipeline and model training are internal assets, this repository showcases the **Productionalization** of those models:

* **Kubernetes (GKE):** Orchestrating microservices to ensure high availability and efficient resource management.
* **Terraform:** Defining the entire GCP environment (Clusters, VPCs, and Node Pools) as code for repeatable, "push-button" deployments.
* **Containerization:** Using optimized Docker images to ensure parity between development and production environments.
* **Internal Networking:** Utilizing Cluster IP services for secure, high-speed internal communication between the web frontend and the prediction engine.

---

## 🚀 Key Engineering Goals
1.  **Scaling:** Transitioning a local ML model into a production-grade GKE deployment.
2.  **IaC (Infrastructure as Code):** Using Terraform to manage complex cloud resources without manual intervention.
3.  **Latency Optimization:** Implementing global caching to optimize inference speed and resource utilization.

---
*Developed by Gurpreet Jagpal - Jagpal Holdings Company*