from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import shutil
import os
from src.services.processors.file_service import VideoProcessor
from schemas.response import AnalysisResponse

router = APIRouter()

# Create a temp folder for uploads
UPLOAD_DIR = "data/uploads"
OUTPUT_DIR = "data/outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@router.post("/video", response_class=FileResponse)
async def analyze_video(file: UploadFile = File(...)):
    """ 
    Endpoint to upload a video and get the analyzed version back
    """
    try:
        # 1. Save the uploaded file temporarily
        input_path = f"{UPLOAD_DIR}/{file.filename}"
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Define Output Path
        output_filename = f"processed_{file.filename}"
        output_path = f"{OUTPUT_DIR}/{output_filename}"
        
        # 3. Run the ML Pipeline
        processor = VideoProcessor()
        # Note : process_video is synchronous, so it might block
        # In real production, we use Celery (Workers). For now, direct call is fine
        processor.process_video(input_path, output_path)
        
        # 4. Return the processed video directly
        return FileResponse(output_path, media_type="video/mp4", filename=output_filename)
    except Exception as e:
        # Clean up if something goes wrong
        if os.path.exists(input_path):
            os.remove(input_path)
        raise HTTPException(status_code=500, detail=str(e))        