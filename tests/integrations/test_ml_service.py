# tests/integrations/test_ml_service.py
import pytest
import numpy as np
from src.ml.pose_estimator import PoseEstimator
from src.core.config import settings
import os

def test_model_file_exists():
    """Check if the .task file actually exists on disk"""
    path = settings.get_model_path()
    assert os.path.exists(path), f"Model file not found at: {path}"

def test_pose_estimator_init():
    """Test if MediaPipe loads without crashing"""
    try:
        estimator = PoseEstimator()
        assert estimator.model is not None
    except Exception as e:
        pytest.fail(f"Failed to initialize PoseEstimator: {e}")

def test_inference_on_dummy_image():
    """
    Create a fake blank image and feed it to the ML model.
    It should return a result object (even if empty).
    """
    estimator = PoseEstimator()
    
    # Create a blank black image (480x640 RGB)
    fake_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    result = estimator.detect(fake_frame)
    
    # We expect a result object, even if no landmarks are found
    assert result is not None
    # Usually pose_landmarks is empty list [] if no person found
    assert hasattr(result, 'pose_landmarks')