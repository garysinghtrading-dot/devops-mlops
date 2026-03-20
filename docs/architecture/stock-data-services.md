# 📈 Stock Data Service: Quantitative Analysis Engine

The **Stock Data Service** is a high-performance microservice designed to provide real-time statistical insights into security price action. It leverages advanced proprietary models to help traders identify structural market imbalances and mean-reversion opportunities.

---

## 🔬 Core Quantitative Indicators

To protect Jagpal Holdings' intellectual property, the specific computational logic is abstracted behind these high-level statistical metrics:

### **1. Regime Equilibrium Offset**
* **Definition**: A measure of the instantaneous spatial divergence between the current market price and the dynamically calculated **stochastic centroid**.
* **Scientific Context**: This metric quantifies the displacement from the primary structural anchor of the current market regime. It identifies when a security has drifted beyond its statistically "stable" zone without revealing the underlying clustering methodology.

### **2. Liquidity Density Gap**
* **Definition**: An analysis of price-action voids relative to **high-order volumetric concentration zones**.
* **Scientific Context**: Rather than focusing on simple trade frequency, this index measures the divergence from areas of maximum historical price-convergence. It highlights "liquidity vacuums" where price discovery is most likely to accelerate or stall.

### **3. Trend Velocity Index**
* **Definition**: The normalized rate of change in price directionality over a rolling temporal window.
* **Scientific Context**: This index provides a dimensionless value representing the "momentum-force" of the current trend, allowing for a standardized comparison of speed across different asset classes.

### **4. Mean Reversion Potential**
* **Definition**: A probabilistic assessment of the price’s **elastic displacement** relative to its established **equilibrium trajectory**.
* **Scientific Context**: This treats price movement as an elastic system returning to a state of lower entropy. It calculates the likelihood of a corrective phase based on how far the current price has deviated from its projected statistical path.

---

## 🏗️ Architectural Implementation

As with our other core services, the Stock Data Service follows a strictly decoupled architecture:

* **GKE Integration**: Deployed as an independent container within the `ml-inference` spot-node pool for cost-optimized scaling.
* **Isolated Logic**: The core mathematical transformations are handled by a "Black Box" logic engine. The public-facing Flask API acts solely as a secure proxy, fetching pre-rendered analytical components via authenticated server-side requests.
* **Data Sourcing**: High-fidelity market data is ingested and processed internally, ensuring that the raw inputs to our proprietary indicators are never exposed to the public internet.

---

## 🔒 Intellectual Property Protection

The HTML templates and scoring logic for this service are hosted in an isolated environment (AWS). The GKE-hosted microservice utilizes a **Server-Side Request Proxy** pattern to retrieve finalized analytical views. 

> **Security Note:** This architecture ensures that even if the container environment is inspected, the underlying "if/then" scoring thresholds, Jinja2 logic, and algorithmic coefficients remain entirely inaccessible to the public.

---
**Developed by** **Gurpreet Singh Jagpal** Founder, Jagpal Holdings Company