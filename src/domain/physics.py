import numpy as np
import math

def get_center_of_mass(landmarks):
    """ Calculates midpoint(COM) of hips (Indices 23 and 24) as center of mass."""
    left_hip = landmarks[23]
    right_hip = landmarks[24]
    
    com_x = (left_hip.x + right_hip.x)/ 2
    com_y = (left_hip.y + right_hip.y)/ 2
    
    return com_x, com_y

def calculate_weight_balance(landmarks, is_right_handed=True):
    """   
    Calculates weight transfer using HEELS for better ground accuracy.
    
    Args:
        landmarks: MediaPipe landmarks
        is_right_handed (bool): True for RH batter, False for LH batter.
    """
    # Use HEELS (29, 30) instead of ankles (27, 28) for better ground contact accuracy
    # Heels are closer to the ground and represent the 'back' of the foot better
    left_heel_x = landmarks[29].x
    right_heel_x = landmarks[30].x
    com_x, _ = get_center_of_mass(landmarks)
    
    # 1. Define Front and Back based on Handedness
    if is_right_handed:
        # RH Batter: Back foot is RIGHT, Front foot is LEFT
        back_foot_x = right_heel_x
        front_foot_x = left_heel_x
    else:
        # LH Batter: Back foot is LEFT, Front foot is RIGHT
        back_foot_x = left_heel_x
        front_foot_x = right_heel_x
        
    # 2. Calculate Stance Width (Base of Support)
    # We use absolute distance because depending on camera angle, 
    # front foot could be left or right of back foot in X-plane.    
    stance_width = abs(front_foot_x - back_foot_x)
    if stance_width < 0.01:
        return 50.0, 50.0
    
    # 3. Calculate Weight Transfer
    # Logic: How far has the COM moved from the Back Foot towards the Front Foot?
    
    # We need the vector distance
    # If standard view (Bowler on Left, Batter on Right)
    # Front Foot X < Back Foot (Front foot is closer to 0)
    
    # Let's use simple Euclidean logic:
    dist_from_back = abs(abs(com_x - back_foot_x))
    
    # Calculate Percentage
    forward_pct = (dist_from_back / stance_width) * 100
    
    # Clip logic (CoM can technically go past the feet, but we cap at 0-100 for UI)
    forward_pct = np.clip(forward_pct, 0, 100)
    back_pct = 100 - forward_pct
    
    return back_pct, forward_pct

def detect_handedness(landmarks):
    """ 
    Automatically detects if batter is Right or  Left handed
    based on which shoulder the chin is closer to.
    
    Returns:
        bool: True for Right-Handed, False for Lef-Handed
    """
    
    # Mediapipe indices
    NOSE = 0
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    
    nose = landmarks[NOSE]
    l_shoulder = landmarks[LEFT_SHOULDER]
    r_shoulder = landmarks[RIGHT_SHOULDER]
    
    # Calculate Euclidean Dsiatnce (2D is sufficient)
    dist_left = math.hypot(nose.x - l_shoulder.x, nose.y - l_shoulder.y)
    dist_right = math.hypot(nose.x - r_shoulder.x, nose.y - r_shoulder.y)
    
    # If nose is closer to Left Shoulder -> Right Handed Batter
    if dist_left < dist_right:
        return True # Right Handed
    else:
        return False # Left Handed 