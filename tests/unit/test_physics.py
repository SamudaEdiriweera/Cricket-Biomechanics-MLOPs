import pytest
from src.domain.physics import calculate_weight_balance, detect_handedness, get_center_of_mass

def test_detect_handness_right(mock_landmarks_rh_stance):
    """ Should correctly identify Right Handed batter """
    is_right_handed = detect_handedness(mock_landmarks_rh_stance)
    assert is_right_handed is True
    
def test_center_of_mass(mock_landmarks_rh_stance):
    """ Should calculate average of hips"""
    com_x, com_y = get_center_of_mass(mock_landmarks_rh_stance)
    expected_com_x = (0.45 + 0.55) / 2
    expected_com_y = (0.5 + 0.5) / 2
    assert com_x == expected_com_x
    assert com_y == expected_com_y
    
def test_weight_balance_neutral(mock_landmarks_rh_stance):
    """
    Test Neutral Balance.
    Back Foot (Right) = 0.7
    Front Foot (Left) = 0.3
    CoM = 0.5 (Exactly in middle)
    Should be 50% Back, 50% Forward
    """
    back_pct, forward_pct = calculate_weight_balance(mock_landmarks_rh_stance, is_right_handed=True) 
    
    assert forward_pct == pytest.approx(50.0)   
    assert back_pct == pytest.approx(50.0) 
    
def test_weight_balance_forward_drive(mock_landmarks_rh_stance):
    """
    Simulate a Forward Defense/Drive.
    Move CoM closer to Front Foot (Left Foot at 0.3).
    """
    # Move Hips to 0.35 (Closer to front foot 0.3)
    mock_landmarks_rh_stance[23].x = 0.30 
    mock_landmarks_rh_stance[24].x = 0.40
    # New CoM = 0.35
    
    back_pct, fwd_pct = calculate_weight_balance(mock_landmarks_rh_stance, is_right_handed=True)
    
    # It should be heavily forward
    assert fwd_pct > 50.0
    assert back_pct < 50.0    