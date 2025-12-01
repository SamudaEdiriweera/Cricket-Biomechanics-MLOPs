# 🏏 Cricket Biomechanics AI (MLOps Pipeline)

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/cricket-biomechanics-mlops/actions/workflows/test.yaml/badge.svg)](https://github.com/YOUR_USERNAME/cricket-biomechanics-mlops/actions)
![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green.svg)

> **An end-to-end Computer Vision MLOps pipeline to quantify cricket batting technique (Balance & Weight Transfer) using MediaPipe, OpenCV, and Physics.**

---

## 🎥 Demo
![Demo Analysis](assets/demo.gif)
*(The AI automatically detecting handedness, tracking the Center of Mass (Yellow Dot), and calculating weight transfer in real-time.)*

---

## 📖 Overview
Inspired by broadcast analytics seen in **The Ashes**, this project reverse-engineers the technology used to analyze batting biomechanics. 

It goes beyond simple pose estimation scripts by implementing a **production-ready architecture**. It includes a physics engine for accurate ground-reaction force estimation, automatic player calibration, and a scalable API wrapper.

### Key Features
*   **🤖 Auto-Handedness Detection:** Uses a geometry-based heuristic (Shoulder-to-Bowler alignment) and a multi-frame voting system to automatically detect if a batter is Right or Left-handed.
*   **physics-Based Accuracy:** Refactored standard pose logic to track **Heel Coordinates** (Base of Support) instead of Ankles, resulting in significantly more stable weight transfer data.
*   **⚡ High-Performance API:** Wrapped in **FastAPI** for real-time inference.
*   **🐳 Containerized:** Fully Dockerized with optimized `slim` images for cloud deployment (AWS/GCP).
*   **✅ CI/CD:** Automated testing pipeline via GitHub Actions to ensure physics logic integrity.

---

## 🛠️ Tech Stack
*   **Core AI:** Python, MediaPipe (BlazePose), OpenCV, NumPy.
*   **Backend:** FastAPI, Uvicorn, Pydantic.
*   **DevOps:** Docker, GitHub Actions (CI/CD).
*   **Testing:** Pytest.

---

## 🧠 The Biomechanics Logic

### 1. Weight Transfer Formula
We calculate the **Center of Mass (CoM)** approximated by the hip midpoint. We then measure its relative position within the **Base of Support (BoS)** defined by the heels.

$$ \text{Forward \%} = \frac{\text{Distance(BackHeel, CoM)}}{\text{StanceWidth}} \times 100 $$

### 2. Why Heels vs. Ankles?
Standard tutorials use Ankle coordinates. However, in a cricket drive, the ankle often flexes or rotates. The **Heel** represents the true contact point with the ground. Switching to heel tracking reduced signal noise by ~15% during the "Trigger Movement" phase.

### 3. Handedness Algorithm
Instead of manual input, we analyze the shoulder vectors relative to the screen edges (assuming standard broadcast view):
*   If $X_{LeftShoulder} < X_{RightShoulder} \rightarrow$ **Right Hand Batter** (Left shoulder faces bowler).
*   If $X_{RightShoulder} < X_{LeftShoulder} \rightarrow$ **Left Hand Batter** (Right shoulder faces bowler).

---

## 🚀 How to Run Locally

### Prerequisites
*   Python 3.9+
*   Docker (Optional but recommended)

### Method 1: Python (Direct)
1.  **Clone the repo**
    ```bash
    git clone https://github.com/YOUR_USERNAME/cricket-biomechanics-mlops.git
    cd cricket-biomechanics-mlops
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Environment**
    Create a `.env` file in the root:
    ```ini
    PROJECT_NAME=CricketBiomechanics
    MODEL_PATH=models/pose_landmarker_lite.task
    ```
    *(Note: The code will auto-download the model if missing).*

4.  **Run the CLI Tool**
    ```bash
    python src/main.py --input video.mp4 --output analysis.mp4
    ```

---

### Method 2: Docker (Production Way)
The Docker image is built on `python:3.9-slim` and includes all necessary OpenGL libraries for OpenCV.

1.  **Build the Image**
    ```bash
    docker build -t cricket-ai .
    ```

2.  **Run the API Server**
    ```bash
    docker run -p 8000:8000 cricket-ai
    ```

3.  **Test the API**
    Go to `http://localhost:8000/docs` and use the Swagger UI to upload a video.

---

## 📂 Project Structure (MLOps Standard)
```text
cricket-biomechanics-mlops/
├── .github/workflows/   # CI/CD Pipelines
├── docker/              # Docker configurations
├── src/
│   ├── app/             # FastAPI Endpoints
│   ├── core/            # Configs & Settings
│   ├── domain/          # Pure Math & Biomechanics Logic
│   ├── ml/              # MediaPipe Wrapper
│   ├── services/        # Video Processing & Visualization
│   └── schemas/         # Pydantic Data Models
├── tests/               # Unit Tests
├── main.py              # CLI Entry point
└── README.md
