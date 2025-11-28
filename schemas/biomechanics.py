"""  
This file defines what a "Biomechanical Analysis" looks 
like in raw numbers. Use this to send data to a 
Frontend to draw charts.
"""

from pydantic import BaseModel
from typing import List, Optional

class KeyPoint(BaseModel):
    name: str
    x: float
    y: float
    confidence: float
    
class FrameAnalysis(BaseModel):
    """ Data for a single frame of video"""
    frame_id: int
    timestamp: float
    weight_back_pct: float
    weight_forward_pct: float
    is_right_handed: bool
    
    # Optional: If you want to send specific coordinates to the frontend
    center_of_mass_x: Optional[float] = None
    
class ShotSummary(BaseModel):
    """Summary of the entire cricket shot"""
    total_frames: int
    max_weight_transfer: float # The peak forward percentage
    avg_balance: float
    handedness: str # "Right" or "Left"
    frame_data: List[FrameAnalysis] # Full timeline of the shot    