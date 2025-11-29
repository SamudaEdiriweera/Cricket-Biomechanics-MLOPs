from fastapi import APIRouter
from src.app.api_v1.endpoints import upload

api_router = APIRouter()

# Include the analyze router
api_router.include_router(upload.router, prefix="/upload", tags=["Uploads"])

