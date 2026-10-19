import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles

MODEL_PATH_HEAVY = "models/pose_landmarker_heavy.task"
MODEL_PATH_FULL = "models/pose_landmarker_full.task"

class MpManager:
    def __init__(self):
        BaseOptions = mp.tasks.BaseOptions
        PoseLandmarker = mp.tasks.vision.PoseLandmarker
        PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode
        
        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=MODEL_PATH_HEAVY),
            running_mode=VisionRunningMode.VIDEO)
        self.landmarker = PoseLandmarker.create_from_options(options)

    def draw_landmarks_on_image(self, rgb_image, frame_timestamp_ms):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        detection_result = self.landmarker.detect_for_video(
            mp_image, frame_timestamp_ms)

        pose_landmarks_list = detection_result.pose_landmarks
        annotated_image = np.copy(rgb_image)
        pose_landmark_style = drawing_styles.get_default_pose_landmarks_style()
        pose_connection_style = drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)
    
        for pose_landmarks in pose_landmarks_list:
            drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=pose_landmarks,
                connections=vision.PoseLandmarksConnections.POSE_LANDMARKS,
                landmark_drawing_spec=pose_landmark_style,
                connection_drawing_spec=pose_connection_style)
    
        return annotated_image

    def close(self):
        self.landmarker.close()