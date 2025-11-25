""" 
We need to be careful here. During a shot (like a spin/pull shot), the head might move.
Best Practice: We should detect the handedness in the first few frames (the stance) and then lock it for the rest of the video. 
If we recalculate it every frame, the labels might flicker.

We will use a "Voting System": Check the first 10 frames, count the votes, and pick the winner.

"""

import cv2
from collections import Counter
from src.ml.pose_estimator import PoseEstimator
from src.domain.physics import calculate_weight_balance, detect_handedness
from src.services.drawing import draw_overlay

class VideoProcessor:
    def __init__(self):
        self.detector = PoseEstimator()
        self.is_right_handed = None # Will be determined automatically
                
    def determine_handedness_voting(self, frames_buffer):
        """
        Analyze first N frames to determine handedness robustly.
        """
        votes = []
        for result in frames_buffer:
            if result.pose_landmarks:
                # Returns True (RH) or False (LH)
                is_rh = detect_handedness(result.pose_landmarks[0])
                votes.append(is_rh)
        
        if not votes:
            return True # Default to RH if detection fails
            
        # Get the most common result
        most_common = Counter(votes).most_common(1)[0][0]
        return most_common
    
    def process_video(self, input_path, output_path):
        cap = cv2.VideoCapture(input_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_count = 0
        calibration_frames = [] # Store results of first 30 frames
        calibration_mode = True
        
        print(f"Processing video: {input_path}")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            frame_count += 1
            if frame_count % 10 == 0:
                print(f"Processing frame {frame_count}/{total_frames}...")

            # RGB Conversion
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # ML Inference
            result = self.detector.detect(frame_rgb)
            
            # --- PHASE 1: CALIBRATION (First 10 Frames) ---
            if calibration_mode:
                calibration_frames.append(result)
                
                # Visual feedback during calibration
                cv2.putText(frame, "Calibrating Player...", (50, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                out.write(frame) # Write the frame as is
                
                if frame_count >= 10:
                    # Lock in the decision
                    self.is_right_handed = self.determine_handedness_voting(calibration_frames)
                    calibration_mode = False
                    player_type = "Right Hand" if self.is_right_handed else "Left Hand"
                    print(f"Detected Player: {player_type}")
                continue # Skip processing this frame, go to next   
                     
            # --- PHASE 2: ANALYSIS (Rest of Video) ---
            back_pct, fwd_pct = 50.0, 50.0
            
            if result.pose_landmarks:
                back_pct, fwd_pct = calculate_weight_balance(
                    result.pose_landmarks[0],
                    is_right_handed=self.is_right_handed
                )
            
            # Visualization
            # Draw (Pass the handedness so visualizer can print it too if needed)
            final_frame = draw_overlay(frame, result, back_pct, fwd_pct)
            
            # Optional: Print detected type on screen
            type_text = "RH Batter" if self.is_right_handed else "LH Batter"
            cv2.putText(final_frame, type_text, (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
            
            out.write(final_frame)  
            
        cap.release()
        out.release()
        print(f"Finished! Saved to {output_path}")      