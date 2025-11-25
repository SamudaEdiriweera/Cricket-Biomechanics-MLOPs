import cv2
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from src.domain.physics import get_center_of_mass

def draw_overlay(image, detection_result, back_pct, forward_pct):
    annotated_image = np.copy(image)
    h, w, _ = annotated_image.shape
    
    if not detection_result.pose_landmarks:
        return annotated_image
    
    # 1. Draw Skeleton
    pose_landmarks = detection_result.pose_landmarks[0]
    proto_list = landmark_pb2.NormalizedLandmarkList()
    proto_list.landmark.extend([
        landmark_pb2.NormalizedLandmark(
            x=l.x, y=l.y, z=l.z
        ) for l in pose_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
        annotated_image,
        proto_list,
        solutions.pose.POSE_CONNECTIONS,
        solutions.drawing_styles.get_default_pose_landmarks_style()
    )
    
    # 2. Draw Center of Mass
    com_x, com_y = get_center_of_mass(pose_landmarks)
    cv2.circle(annotated_image, (int(com_x * w), int(com_y * h)), 15, (0, 255, 255), -1)
    
    # 3. Draw Bar
    bar_x, bar_y, bar_w, bar_h = 50, h - 100, 400, 40
    split_point = int((back_pct / 100) * bar_w)
    
    # Red (Back) and Blue (Forward)
    cv2.rectangle(annotated_image, (bar_x, bar_y), (bar_x + split_point, bar_y + bar_h), (0, 0, 255), -1)
    cv2.rectangle(annotated_image, (bar_x + split_point, bar_y), (bar_x + bar_w, bar_y + bar_h), (255, 150, 0), -1)
    cv2.rectangle(annotated_image, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (255, 255, 255), 3)  
    
    # Text
    cv2.putText(annotated_image, f"{int(back_pct)}% BACK", (bar_x, bar_y + 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(annotated_image, f"FORWARD {int(forward_pct)}%", (bar_x + 200, bar_y + 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 150, 0), 2)  
    
    return annotated_image  