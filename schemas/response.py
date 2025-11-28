from pydantic import BaseModel
from schemas.biomechanics import ShotSummary
from schemas.video import VideoMetadata

class AnalysisResponse(BaseModel):
    status: str
    video_info: VideoMetadata
    biomechanics: ShotSummary
    download_url: str