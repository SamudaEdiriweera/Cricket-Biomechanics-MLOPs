from fastapi import FastAPI
from src.app.api_v1.router import api_router
from src.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json"
)

# Include Routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Cricket Biomechanics AI is Running 🚀"}