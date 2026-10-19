import sys
import time
import cv2
from MpManager import MpManager

VIDEO_PATH = "videos/Snatch.MOV"

class VideoScanner:
    def __init__(self):
        self.cap = cv2.VideoCapture(VIDEO_PATH)
        if not self.cap.isOpened():
            print("Error: could not open the video file.")
            sys.exit(1)
        print("Video file opened successfully.")
        
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
        self.frame_duration = 1 / self.fps

        self.start_time = None
        self.frame_index = 0
        self.mp = MpManager()
        self.closed = False

    def show_next_frame(self):
        if self.closed:
            return None

        if self.start_time is None:
            self.start_time = time.perf_counter()
        
        elapsed_s = time.perf_counter() - self.start_time
        expected_index = int(elapsed_s / self.frame_duration)

        while self.frame_index < expected_index:
            if not self.cap.grab():
                self.close()
                return None
            self.frame_index += 1

        ret, frame = self.cap.read()
        if not ret:
            self.close()
            return None
        self.frame_index += 1

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.mp.draw_landmarks_on_image(frame, int(self.frame_index * 1000 / self.fps))

    def close(self):
        if self.closed:
            return

        self.closed = True
        self.cap.release()
        self.mp.close()
