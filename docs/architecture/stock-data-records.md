# Jagpal Holdings Company – Stock Trade Records Microservice

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Microframework-lightgrey.svg)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue.svg)
![SQLite](https://img.shields.io/badge/SQLite-Embedded%20DB-003B57.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)
![License](https://img.shields.io/badge/License-Proprietary-red.svg)

This microservice provides a lightweight, demo‑friendly system for tracking client stock positions. It maintains accurate share quantities and cost basis using **FIFO (First‑In, First‑Out)** accounting, mirroring real-world brokerage tax lot tracking.

While the production version utilizes **Azure Database**, this demonstration version is built with **Python Flask** and **SQLite**, fully containerized with **Docker** for seamless deployment.

---

## 📊 Overview

This microservice enables users to:
* **Portfolio Tracking:** View all current security holdings.
* **Performance Metrics:** See total shares and average cost per ticker.
* **Trade Execution:** Log new buy or sell transactions.
* **Automated Accounting:** Recalculate cost basis automatically using FIFO rules.
* **Validation:** Prevent short selling (selling more shares than currently owned).

> **Note:** For demo consistency, the SQLite database (`records/demo.db`) is baked into the Docker image. Each container run starts with a clean, predictable dataset.

---

## 🧮 Cost Basis Calculation

The average cost is computed using the following formula:

$$\text{Average Cost} = \frac{\sum(\text{shares purchased} \times \text{price})}{\text{total shares}}$$

When shares are sold, the system removes the oldest shares first (**FIFO**). The remaining lots are then used to determine the updated average cost for the position.

---

## 🖥️ Application Behavior

### User Interface
* **Landing Page:** Displays the current user (`demo_user`) and a summary table of held securities, total shares, and average cost.
* **Trade Submission:** A simple interface to select **Buy** or **Sell**, input quantity, and set the price.

### Backend Logic
1.  **Validation:** Checks share availability for sell orders.
2.  **Persistence:** Updates the local SQLite instance.
3.  **Calculation:** Triggers the `HandleTradeService` to re-calculate positions.
4.  **Refresh:** Redirects to the landing page with updated real-time data.

---

## 🧱 Technology Stack

* **Language:** Python 3.11
* **Framework:** Flask
* **Database:** SQLite (Demo) / Azure Database (Production)
* **Deployment:** Docker

---

## 📦 Deployment

### Build the Image
```bash
docker build -t stock-service .

## 📦 Running the Service with Docker

Build the image:
```bash
docker build -t stock-service .

Run the container:

```bash
docker run -p 5000:5000 stock-service

## 🗂️ Project Structure

```text
.
├── app.py
├── HandleTradeService.py
├── Dockerfile
├── requirements.txt
├── templates/
│   └── landing.html
└── records/
    └── create-demo_db.py
    └── demo.db
## 🧪 Database Initialization
The repository includes an optional `create_db.py` script used to generate the initial `demo.db` file. This script is not executed inside Docker and is included only for transparency and reproducibility.

---

## 👤 Developed By
**Gurpreet Jagpal** Jagpal Holdings Company  
*March 23, 2026*