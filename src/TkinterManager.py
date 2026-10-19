import time

import tkinter as tk
from PIL import Image, ImageTk
from VideoScanner import VideoScanner

class TkinterManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weightlifting Scanner")

        self._screen_width = self.root.winfo_screenwidth()
        self._screen_height = self.root.winfo_screenheight()

        self._window_width = self._screen_width // 4
        self._window_height = self._screen_height // 3

        self.root.geometry(f'{self._window_width}x{self._window_height}')

        self.video_label = tk.Label(self.root)
        self.video_label.pack(side="left")
        self.analyse_label = tk.Label(self.root)
        self.analyse_label.pack(side="right")
        self.vs = VideoScanner()
        self._after_id = None
        self._closed = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        if self._closed:
            return

        self._closed = True
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)
            self._after_id = None
        self.vs.close()
        self.root.destroy()

    def run(self):
        if self._closed:
            return

        frame_img = self.vs.show_next_frame()
        if (frame_img is None):
            self.close()
            return
        frame_img = Image.fromarray(frame_img)
        frame_img.thumbnail((self._window_width // 2, self._window_height), Image.Resampling.BILINEAR)
        frame_photo = ImageTk.PhotoImage(image=frame_img)
        self.video_label.config(image=frame_photo)
        self.video_label.image = frame_photo

        next_deadline = self.vs.start_time + self.vs.frame_index * self.vs.frame_duration
        wait_ms = max(1, int((next_deadline - time.perf_counter()) * 1000))
        self._after_id = self.root.after(wait_ms, self.run)