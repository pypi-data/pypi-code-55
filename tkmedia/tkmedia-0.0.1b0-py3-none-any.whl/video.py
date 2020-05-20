import tkinter
from tkinter import ttk
import imageio
from PIL import ImageTk, Image
import time
from . import audio
import threading
from imageio.plugins.ffmpeg import FfmpegFormat

class Video():
    def __init__(self):
        self.audio = audio.audio()
        format = FfmpegFormat(
            "ffmpeg",
            "Many video formats and cameras (via ffmpeg)",
            ".mov .avi .mpg .mpeg .mp4 .mkv .wmv .webm",
            "I",
            )
        imageio.formats.add_format(format,True)
    def openfile(self, file_path):
        try:
            self.video = imageio.get_reader(file_path)
        except imageio.core.fetching.NeedDownloadError:
            imageio.plugins.avbin.download()
            self.video = imageio.get_reader(file_path)
        self.audio.openfile(file_path)
    
    def play(self, frame, place=0):
        self.frame = frame
        self.frame.vidframe = ttk.Label(self.frame)
        self.frame.vidframe.pack(fill="both",expand=True)
        self.video_thread = threading.Thread(target=self._stream,args=(place,))
        self.video_thread.start()
    
    def stop(self):
        self.audio.stop()
        self.video_thread.stop()
    def goto(self,place):
        pass
    def goto_audio(self,place):
        self.audio.goto(int(place/10))
    def close(self):
        pass
    def _stream(self,place):
        self.audio.play()
        start_time=time.time()
        sleeptime = 1/self.video.get_meta_data()["fps"]
        frame_now = 0
        for image in self.video.iter_data():
            frame_now = frame_now + 1
            if frame_now*sleeptime >= place:
                if frame_now*sleeptime >= time.time()-start_time:
                    frame_image = ImageTk.PhotoImage(Image.fromarray(image).resize((int(self.frame.winfo_width()),int(self.frame.winfo_height())),Image.BOX),master=self.frame)
                    self.frame.vidframe.config(image=frame_image)
                    self.frame.vidframe.image = frame_image
                    time.sleep(sleeptime)
                else:
                    pass
            else:
                pass
