import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from src.core.config import settings

class PoseEstimator:
    def __init__(self):
        # Use the dynamic path method
        model_path = settings.get_model_path()
        
        print(f"Loading Pose Landmarker model from: {model_path}")
        
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=False,
        )
        self.model = vision.PoseLandmarker.create_from_options(options)
        
        
    def detect(self, frame_rgb):
        # convert numpy array to MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        return self.model.detect(mp_image)