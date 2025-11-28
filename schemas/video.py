""" 
This file handles validation for video properties. 
It helps ensure the user doesn't upload a corrupted file or a 
4K movie that crashes your server.
"""

from pydantic import BaseModel

class VideoMetadata(BaseModel):
    filename: str
    content_type: str
    size_mb: float
    resolution_width: int
    resolution_height: int
    fps: int
    duration_seconds: float
    
class VideoUploadRequest(BaseModel):
    """ Used if you want to validate headers before processing """
    filename: str
    expected_size: str
    
    