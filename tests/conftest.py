import pytest
from dataclasses import dataclass

@dataclass
class MockLandmark:
    x: float
    y: float
    z: float = 0.0
    
@pytest.fixture
def mock_landmarks_rh_stance():
    """ 
    Creates a list of 33 fake landmarks representing a
    Rigth-Handed Batter in a neutral stance.
    """
    # Initialize a list of 33 landmarks with default values
    landmarks = [MockLandmark(x=0.5, y=0.5)] * 33 # Initialize all
    
    # --- 1. SETUP FOR HANDEDNESS (Chin-to-Shoulder Logic) ---
    # Shoulders positions
    landmarks[11] = MockLandmark(x=0.4, y=0.3) # Left Shoulder
    landmarks[12] = MockLandmark(x=0.6, y=0.3) # Right Shoulder

    # Nose Position (Crucial for your logic)
    # Move Nose closer to Left Shoulder (0.4) to simulate RH Batter looking at bowler
    landmarks[0]  = MockLandmark(x=0.42, y=0.25) 
    
    # 2. Setup Hips for CoM (Center of Mass)
    landmarks[23] = MockLandmark(x=0.45, y=0.5) # Left Hip
    landmarks[24] = MockLandmark(x=0.55, y=0.5) # Right Hip
    # Com x = 0.5
    
    # 3. Setup Feet (Heels)
    # RH Batter: Left foot (front) at 0.3, Right foot (back) at 0.7
    # Stance width = 0.4
    landmarks[29] = MockLandmark(x=0.3, y=0.9) # Left Heel (Front)
    landmarks[30] = MockLandmark(x=0.7, y=0.9) # Right Heel (Back)
    
    return landmarks
    
@pytest.fixture
def mock_landmarks_lh_stance():
    """
    Creates a mock set of landmarks for a Left-Handed Batter.
    """
    landmarks = [MockLandmark(x=0.5, y=0.5)] * 33
    
    # Shoulders
    landmarks[11] = MockLandmark(x=0.4, y=0.3) 
    landmarks[12] = MockLandmark(x=0.6, y=0.3) 
    
    # Nose Position 
    # Move Nose closer to Right Shoulder (0.6) to simulate LH Batter
    landmarks[0]  = MockLandmark(x=0.58, y=0.25)
    
    # Heels (Inverted for LH)
    landmarks[29] = MockLandmark(x=0.3, y=0.9) # Left Heel (Back)
    landmarks[30] = MockLandmark(x=0.7, y=0.9) # Right Heel (Front)
    
    return landmarks