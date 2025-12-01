from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.app.api_v1.router import api_router
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json"
)

# --- 1. ENABLE CORS (CRITICAL FOR NEXT.JS) ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. MOUNT STATIC FILES ---
# This allows Next.js to access processed videos via URL
# e.g., http://localhost:8000/static/processed_vk.mp4
app.mount("/static", StaticFiles(directory="data/outputs"), name="static")

# Include Routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Cricket Biomechanics AI is Running 🚀"}