import cv2
from src.ml.pose_estimator import PoseEstimator
from src.domain.physics import calculate_weight_balance
from src.services.drawing import draw_overlay

class StreamProcessor:
    def __init__(self, source=0):
        # Source can be 0 (Webcam), 1 (External Cam), or "rtsp://ip:port"
        self.source = source
        self.detector = PoseEstimator()

    def generate_frames(self):
        """
        Generator function for Web Streaming.
        It yields bytes instead of saving a file.
        """
        cap = cv2.VideoCapture(self.source)
        
        if not cap.isOpened():
            raise ValueError(f"Could not open video source: {self.source}")

        while True:
            success, frame = cap.read()
            if not success:
                break

            # 1. Process (Same logic as file service)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.detector.detect(frame_rgb)
            
            back_pct, fwd_pct = 50.0, 50.0
            if result.pose_landmarks:
                back_pct, fwd_pct = calculate_weight_balance(result.pose_landmarks[0])

            # 2. Draw
            annotated_frame = draw_overlay(frame, result, back_pct, fwd_pct)

            # 3. Encode for Web (JPEG format)
            # We don't save to MP4, we convert to JPEG bytes for the browser
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_bytes = buffer.tobytes()

            # 4. Yield the frame (This is the Magic part for Streaming)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        cap.release()