from fastapi import APIRouter, UploadFile, File, HTTPException, Request
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

@router.post("/video")
async def analyze_video(request: Request, file: UploadFile = File(...)):
    """ 
    Endpoint to upload a video and get the analyzed version back
    """
    try:
        # 1. Save the uploaded file temporarily
        input_path = f"{UPLOAD_DIR}/{file.filename}"
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Define Output Path
        # output_filename = f"processed_{file.filename}"
        filename_without_ext = os.path.splitext(file.filename)[0]
        output_filename = f"processed_{filename_without_ext}.webm"
        output_path = f"{OUTPUT_DIR}/{output_filename}"
        
        # 3. Run the ML Pipeline
        processor = VideoProcessor()
        # Note : process_video is synchronous, so it might block
        # In real production, we use Celery (Workers). For now, direct call is fine
        processor.process_video(input_path, output_path)
        
        # 4. Extract Player Type
        # The processor instance holds the state after running process_video
        player_type = "Unknown"
        if processor.is_right_handed is True:
            player_type = "Right Hand Batter"
        elif processor.is_right_handed is False:
            player_type = "Left Hand Batter"
            
        print("###################test1#######")
        # 5. Generate URL for Next.js
        # ✅ FIX 2: Handle trailing slash safely
        # request.base_url returns "http://127.0.0.1:8001/" (with slash)
        base_url = str(request.base_url).rstrip("/") 
        print("###################test2#######")
        video_url = f"{base_url}/static/{output_filename}"
        print(video_url)
        print("###################test3#######")
        
        # 4. Return the processed video directly
        return {
            "status": "success",
            "video_url": video_url,
            "filename": output_filename,
            "player_type": player_type  # <--- ✅ ADDED THIS
            # If you updated your processor to return stats, add them here:
            # "stats": processor.get_stats()             
        }
    except Exception as e:
        # Clean up if something goes wrong
        if os.path.exists(input_path):
            os.remove(input_path)
        raise HTTPException(status_code=500, detail=str(e))        