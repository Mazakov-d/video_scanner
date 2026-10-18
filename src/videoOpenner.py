#!/usr/bin/env python3

import tkinter as tk
import cv2
from PIL import Image, ImageTk

VIDEO_PATH = "../lift_video.mp4"   # or 0 for your webcam

root = tk.Tk()
root.title("Video player")

label = tk.Label(root)
label.pack()

cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
delay = int(1000 / fps)       # milliseconds between frames

def show_next_frame():
    ok, frame = cap.read()
    if not ok:                # end of the video
        cap.release()
        return

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   # OpenCV uses BGR, Pillow uses RGB
    img = ImageTk.PhotoImage(Image.fromarray(frame))

    label.config(image=img)
    label.image = img         # keep a reference, or the image disappears

    root.after(delay, show_next_frame)  # schedule the next frame

show_next_frame()
root.mainloop()