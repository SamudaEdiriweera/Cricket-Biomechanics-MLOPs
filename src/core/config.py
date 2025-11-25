import os
from pydantic_settings import BaseSettings
from pathlib import Path

# Get the Project Root Directory (one level up from 'src)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "CricketBiomechanics"
    MODEL_PATH_LITE: str = "models/pose_landmarker_lite.task"
    MODEL_PATH_HEAVY: str = "models/pose_landmarker_heavy.task"
    
    # Default configurations
    CONFIDENCE_THRESHOLD: float = 0.5
    
    def get_model_path(self) -> str:
        # This ensures it works locally AND in Docker
        return str(BASE_DIR / self.MODEL_PATH_HEAVY)
    
    class Config: 
        env_file = ".env"
        
settings = Settings()
