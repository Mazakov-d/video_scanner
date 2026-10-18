#!/usr/bin/env python3

import sys
import time
import tkinter as tk
import cv2
from PIL import Image, ImageTk

VIDEO_PATH = "../weightlifting_video.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("Error: could not open video file.")
    sys.exit(1)                                  # CHANGED: stop here instead of continuing
print("Video file opened successfully!")

fps = cap.get(cv2.CAP_PROP_FPS) or 30
frame_duration_s = 1 / fps                       # CHANGED: duration of one frame, in seconds

root = tk.Tk()
root.title("Video Scanner")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = screen_width // 4
window_height = screen_height // 3

root.geometry(f'{window_width}x{window_height}')

label = tk.Label(root)
label.pack(side="left")

start_time = None                                # NEW: set when playback really starts
frame_index = 0                                  # NEW: number of the next frame to show

def show_next_frame():
    global start_time, frame_index

    # NEW: start the clock on the first call
    if start_time is None:
        start_time = time.perf_counter()

    # NEW: which frame should be on screen right now?
    elapsed_s = time.perf_counter() - start_time
    expected_index = int(elapsed_s / frame_duration_s)

    # NEW: if we're late, skip frames without decoding them
    while frame_index < expected_index:
        if not cap.grab():
            cap.release()
            return
        frame_index += 1

    ret, frame = cap.read()
    if not ret:
        cap.release()
        return
    frame_index += 1                             # NEW

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_img = Image.fromarray(frame)
    frame_img.thumbnail((window_width // 2, window_height), Image.Resampling.BILINEAR)
    frame_photo = ImageTk.PhotoImage(image=frame_img)
    label.config(image=frame_photo)
    label.image = frame_photo

    # NEW: wait until the next frame's deadline
    next_deadline = start_time + frame_index * frame_duration_s
    wait_ms = max(1, int((next_deadline - time.perf_counter()) * 1000))
    root.after(wait_ms, show_next_frame)

show_next_frame()
root.mainloop()