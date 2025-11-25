# cricket-biomechanics-mlops
An end-to-end Computer Vision pipeline using Deep Learning-based for analyzing cricket batting biomechanics (weight transfer, balance). Built with Python, MediaPipe, FastAPI, Docker, and deployed with CI/CD.

```bash
cricket-analyzer-pro/
├── .github/                       # CI/CD Pipelines
│   └── workflows/
│       ├── tests.yaml             # Auto-run tests on git push
│       └── deploy_docker.yaml     # Build & Push Docker image to Cloud
│
├── config/                        # Deployment Configs
│   ├── gunicorn_conf.py           # Production server settings (workers, threads)
│   └── logging.yaml               # structured logging rules
│
├── data/                          # Local Development Data (Ignored by Git)
│   ├── uploads/                   # Raw user videos
│   └── processed/                 # Output videos with overlay
│
├── docker/                        # Containerization
│   ├── Dockerfile                 # The instructions to build the image
│   └── docker-compose.yaml        # Run App + Redis + Prometheus locally
│
├── src/                           # SOURCE CODE
│   ├── app/                       # API Layer (FastAPI)
│   │   ├── __init__.py
│   │   ├── main.py                # App Entry Point (The 'run' file)
│   │   ├── api_v1/                # API Version 1
│   │   │   ├── __init__.py
│   │   │   ├── router.py          # Main router
│   │   │   └── endpoints/
│   │   │       ├── upload.py      # POST /analyze/file (Batch processing)
│   │   │       └── stream.py      # GET /analyze/stream (Live Webcam)
│   │   └── middleware.py          # CORS, Auth, Rate Limiting
│   │
│   ├── core/                      # Global Configuration
│   │   ├── __init__.py
│   │   ├── config.py              # Environment Variables (Pydantic Settings)
│   │   └── exceptions.py          # Custom Error Handling
│   │
│   ├── domain/                    # PURE MATH (No OpenCV/MediaPipe here)
│   │   ├── __init__.py
│   │   ├── physics.py             # Functions: get_com(), calc_weight_transfer()
│   │   └── rules.py               # Logic: "Is this a cover drive?"
│   │
│   ├── ml/                        # AI Model Wrappers
│   │   ├── __init__.py
│   │   └── pose_estimator.py      # Class wrapper for MediaPipe Landmarker
│   │
│   ├── schemas/                   # Data Validation (Pydantic)
│   │   ├── __init__.py
│   │   ├── biomechanics.py        # Output format (JSON structure for frontend)
│   │   └── video.py               # Input validation (File size, type)
│   │
│   └── services/                  # Application Logic (The "Glue")
│       ├── __init__.py
│       ├── drawing.py             # Drawing Skeleton, Bar, Text (Visualizer)
│       ├── file_service.py        # Logic to process MP4 -> MP4
│       └── stream_service.py      # Logic to yield frames -> Browser
│
├── tests/                         # Test Suite
│   ├── unit/                      # Test domain math & ML wrapper
│   └── integration/               # Test API endpoints
│
├── .dockerignore                  # Files to exclude from Docker image
├── .env                           # Secrets & Keys (API Keys, Model Paths)
├── .gitignore                     # Git exclusions
├── Makefile                       # Shortcuts (e.g., 'make run', 'make test')
├── pyproject.toml                 # Dependencies (Poetry)
└── README.md                      # Documentation