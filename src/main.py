#!/usr/bin/env python3

from TkinterManager import TkinterManager

if __name__ == "__main__":
    tkm = TkinterManager()
    tkm.run()
    tkm.root.mainloop()


# import sys
# import time
# import tkinter as tk
# from pathlib import Path

# import cv2
# import mediapipe as mp
# import numpy as np
# from PIL import Image, ImageTk
# from mediapipe.tasks.python import vision
# from mediapipe.tasks.python.vision import drawing_utils
# from mediapipe.tasks.python.vision import drawing_styles

# BASE_DIR = Path(__file__).resolve().parent.parent
# MODEL_PATH = BASE_DIR / "models/pose_landmarker_heavy.task"
# VIDEO_PATH = BASE_DIR / "Snatch.MOV"

# cap = cv2.VideoCapture(str(VIDEO_PATH))
# if not cap.isOpened():
#     print("Error: could not open video file.")
#     sys.exit(1)
# print("Video file opened successfully!")

# fps = cap.get(cv2.CAP_PROP_FPS) or 30
# frame_duration_s = 1 / fps

# root = tk.Tk()
# root.title("Video Scanner")

# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()

# window_width = screen_width // 4
# window_height = screen_height // 3

# root.geometry(f'{window_width}x{window_height}')

# label = tk.Label(root)
# label.pack(side="left")

# start_time = None
# frame_index = 0


# # BaseOptions = mp.tasks.BaseOptions
# # PoseLandmarker = mp.tasks.vision.PoseLandmarker
# # PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
# # VisionRunningMode = mp.tasks.vision.RunningMode

# # options = PoseLandmarkerOptions(
# #     base_options=BaseOptions(model_asset_path=str(MODEL_PATH)),
# #     running_mode=VisionRunningMode.VIDEO)
# # landmarker = PoseLandmarker.create_from_options(options)


# # def draw_landmarks_on_image(rgb_image, detection_result):
# #     pose_landmarks_list = detection_result.pose_landmarks
# #     for i, landmark in enumerate(pose_landmarks_list[0]):
# #         print(i, landmark.x, landmark.y, landmark.z)
# #     sys.exit(0)
# #     annotated_image = np.copy(rgb_image)

# #     pose_landmark_style = drawing_styles.get_default_pose_landmarks_style()
# #     pose_connection_style = drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)

# #     for pose_landmarks in pose_landmarks_list:
# #         drawing_utils.draw_landmarks(
# #             image=annotated_image,
# #             landmark_list=pose_landmarks,
# #             connections=vision.PoseLandmarksConnections.POSE_LANDMARKS,
# #             landmark_drawing_spec=pose_landmark_style,
# #             connection_drawing_spec=pose_connection_style)

# #     return annotated_image

# def show_next_frame():
#     global start_time, frame_index
#     if start_time is None:
#         start_time = time.perf_counter()

#     elapsed_s = time.perf_counter() - start_time
#     expected_index = int(elapsed_s / frame_duration_s)

#     while frame_index < expected_index:
#         if not cap.grab():
#             cap.release()
#             return
#         frame_index += 1

#     ret, frame = cap.read()
#     if not ret:
#         cap.release()
#         landmarker.close()
#         root.destroy()
#         return
#     frame_index += 1

#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
#     pose_landmarker_result = landmarker.detect_for_video(
#         mp_image, int(frame_index * 1000 / fps))
#     frame = draw_landmarks_on_image(frame, pose_landmarker_result)
#     frame_img = Image.fromarray(frame)
#     frame_img.thumbnail((window_width // 2, window_height), Image.Resampling.BILINEAR)
#     frame_photo = ImageTk.PhotoImage(image=frame_img)
#     label.config(image=frame_photo)
#     label.image = frame_photo

#     next_deadline = start_time + frame_index * frame_duration_s
#     wait_ms = max(1, int((next_deadline - time.perf_counter()) * 1000))
#     root.after(wait_ms, show_next_frame)


# def close_video():
#     cap.release()
#     landmarker.close()
#     root.destroy()


# root.protocol("WM_DELETE_WINDOW", close_video)

# show_next_frame()
# root.mainloop()