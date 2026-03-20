# Stock Data Service

## 🧩 Overview

The Stock Data Service is a stateless microservice responsible for retrieving server-rendered market data views from an AWS-hosted backend.

It operates strictly as a transport layer between clients and the rendering system, with no embedded business logic or market data processing.

## 🏗️ Architecture

The service follows a clear separation between request handling and computation.

**Request Flow:**

1. A client sends a request with query parameters (e.g., symbol or identifier)
2. The Stock Data Service forwards the request to a designated AWS endpoint
3. The AWS backend performs all computation and conditional logic
4. A fully rendered HTML response is returned to the service
5. The service relays the response back to the client


## 🔒 Separation of Responsibilities

The system is designed to enforce strict boundaries between infrastructure and proprietary logic.

### Stock Data Service
- Handles inbound HTTP requests
- Forwards query parameters to AWS
- Returns rendered HTML responses
- Maintains no local state or computation

### AWS Backend
- Executes all business logic and conditional processing
- Performs market data analysis and transformations
- Generates final rendered outputs

## 🛡️ Intellectual Property Protection

Jagpal Holdings enforces a server-side execution model to protect proprietary algorithms and market-state logic.

Within the Stock Data Service:

- No business logic, scoring rules, or conditional branches are implemented
- No model parameters, thresholds, or transformations are present
- No intermediate computation states are stored, logged, or exposed

All sensitive processing occurs exclusively within the AWS backend.

As a result:

- Clients interact only with final rendered outputs
- The service provides no direct visibility into internal decision-making
- Proprietary logic remains isolated from this layer by design

## ⚙️ Infrastructure

The service is deployed using Terraform as part of a broader microservices architecture.

Key characteristics:
- Stateless design for horizontal scalability
- Clear isolation of responsibilities across services
- Secure boundary between public-facing infrastructure and private computation layers

## 📌 Design Notes

- This service is intentionally minimal and should not contain business logic
- Any changes to computation or decision-making must be implemented in the AWS backend
- The service should be treated as a stable interface layer within the system architecture

---
**Developed by** **Gurpreet Singh Jagpal** Founder, Jagpal Holdings Company
