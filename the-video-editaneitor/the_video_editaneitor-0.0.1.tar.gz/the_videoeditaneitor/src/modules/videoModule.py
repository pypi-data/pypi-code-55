import os
import threading

import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import numpy as np
import pygame as pg
import pygame_gui as pgu
from moviepy.editor import VideoFileClip
from pyAudioAnalysis import audioBasicIO as aIO
from datetime import datetime
import json


class VideoModule:

    def __init__(self, _manager, dest=(0, 0), size=(800, 600)):
        self.manager = _manager
        self.dest = dest
        self.size = size

        self.video_panel = pgu.elements.UIPanel(
            manager=self.manager,
            starting_layer_height=0,
            relative_rect=pg.Rect(self.dest, self.size))

        self.img_video_frame = None
        self.img_graph_frame = None
        self.path_video = None
        self.clean()

        self.wnd_Loading:pgu.elements.ui_window.UIWindow = None
        self.is_loaded_video = True

    def clean(self):
        self.actual_frame = 0
        self.is_play = False
        self.is_one_frame = False
        self.general_frame_ini = 0
        self.general_frame_end = 0
        self.selected_frame_ini = 0
        self.selected_frame_end = 0
        self.clip = None
        self.fps = 30
        self.exported_date = None

    def set_path_video(self, _path_video):
        if self.path_video != _path_video:
            self.path_video = _path_video
            self.is_loaded_video = False
            self.wnd_Loading = pgu.elements.ui_window.UIWindow(
                rect=pg.Rect(self.dest, self.size),
                manager=self.manager,
                window_display_title="Loading")

    def __load_video(self):
        if not self.is_loaded_video:
            self.is_loaded_video = True
            self.clean()
            self.load_export_data()

            if self.path_video is not None:
                width = self.size[0] - 5
                height = self.size[1] - 10

                # Read and resize the video file
                self.clip = VideoFileClip(self.path_video).resize(width=width)
                self.fps = self.clip.fps

                label_dest = (0, 0)
                label_size = (width, 60)

                video_dest = (0, label_size[1])

                graphic_dest = (0, label_size[1] + self.clip.size[1] + 5)
                graphic_size = (width, height - (label_size[1] + self.clip.size[1] + 5))

                self.flags = {
                    "video": threading.Event(),
                    "sound": threading.Event(),
                    "graph": threading.Event(),
                    "time": threading.Event()
                }

                pgu.elements.UITextBox(html_text=self.path_video, manager=self.manager, container=self.video_panel,
                                     relative_rect=pg.Rect(label_dest, label_size))

                # launch the thread
                threading.Thread(target=self.preview_video, args=(video_dest, self.clip.size), daemon=True).start()
                if self.clip.audio:
                    threading.Thread(target=self.preview_sound, daemon=True).start()
                    threading.Thread(target=self.preview_graph, args=(graphic_dest, graphic_size), daemon=True).start()

                # wait the creation of the frames in video, graph and audio
                self.flags["video"].wait(2.0)
                self.flags["sound"].wait(2.0)
                self.flags["graph"].wait(5.0)

                # self.clip.close()

                self.flags["time"].clear()

                self.general_frame_end = int(self.fps * self.clip.duration)
                if self.selected_frame_end == 0:
                    self.selected_frame_end = int(self.fps * self.clip.duration)

            self.wnd_Loading.kill()

    def preview_video(self, dest=(0, 0), size=(100, 100)):

        print("vm {}".format(self.actual_frame))
        chunks = []
        for t in np.arange(1.0 / self.fps, self.clip.duration + .001, 1.0 / self.fps):
            img = self.clip.get_frame(t)
            chunks.append(pg.surfarray.make_surface(img.swapaxes(0, 1)))

        self.img_video_frame = pgu.elements.UIImage(
            relative_rect=pg.Rect(dest, size),
            image_surface=chunks[0],
            manager=self.manager,
            container=self.video_panel)

        prev_frame = self.actual_frame
        self.flags["video"].set()
        while self.flags["time"] is not None and self.flags["video"] is not None:
            # print("videoFlag.set()")
            self.flags["time"].wait()
            # print("timeFlag.wait video end")
            if prev_frame is not self.actual_frame - 1:
                prev_frame = self.actual_frame - 1
                print("video frame " + str(self.actual_frame - 1))
                self.img_video_frame.set_image(chunks[self.actual_frame - 1])

    def preview_sound(self, nbytes=2):
        audio = self.clip.audio

        pg.mixer.quit()
        pg.mixer.init(self.clip.audio.fps, -8 * nbytes, audio.nchannels, 1024)

        audio_frames_by_video_frame = round(audio.fps / self.fps)

        total_size = round(audio.fps * self.clip.duration)
        pospos = np.array(list(range(0, total_size, audio_frames_by_video_frame)) + [total_size])

        chunks = []
        for i in range(0, len(pospos) - 1):
            tt = (1.0 / audio.fps) * np.arange(pospos[i], pospos[i + 1])
            sound_array = audio.to_soundarray(tt, nbytes=nbytes, quantize=True)
            chunks.append(pg.sndarray.make_sound(sound_array))

        channel = None
        prev_frame = self.actual_frame
        self.flags["sound"].set()
        while self.flags["time"] is not None and self.flags["sound"] is not None:
            # print("audioFlag.set()")
            self.flags["time"].wait()
            # print("timeFlag.wait() audio end")
            if prev_frame is not self.actual_frame:
                prev_frame = self.actual_frame
                print("sound frame " + str(self.actual_frame))
                if channel is None or channel.get_queue():
                    channel = chunks[self.actual_frame].play()
                else:
                    channel.queue(chunks[self.actual_frame])

    def preview_graph(self, dest=(0, 0), size=(300, 400)):
        path_audio = os.path.abspath(os.getcwd()) + "\\temp.wav"

        # Write an Audio file
        audio = self.clip.audio
        audio.write_audiofile(path_audio)

        # Generate the wave to the graphic
        sampling_rate, signal = aIO.read_audio_file(path_audio)

        # calculate the time range
        time_x = np.arange(0, signal.shape[0] / float(sampling_rate), 1.0 / sampling_rate)

        audio_frames_by_video_frame = int(audio.fps / self.fps)

        chunks = []
        for x in time_x[::audio_frames_by_video_frame]:
            fig, _ax = plt.subplots()
            fig.set_figheight(size[1] / 100)
            fig.set_figwidth(size[0] / 100)

            _ax.plot(time_x, signal)

            for y in time_x[::audio_frames_by_video_frame]:
                _ax.axvline(y, color="red", alpha=0.2)

            _ax.axvline(x, color="blue", alpha=0.7)
            canvas = agg.FigureCanvasAgg(fig)
            canvas.draw()
            raw_data = canvas.get_renderer().tostring_rgb()
            canvas_size = canvas.get_width_height()
            graphic = pg.image.fromstring(raw_data, canvas_size, "RGB")
            chunks.append(graphic)

        self.img_graph_frame = pgu.elements.UIImage(
            relative_rect=pg.Rect(dest, size),
            image_surface=chunks[0],
            manager=self.manager,
            container=self.video_panel)

        prev_frame = self.actual_frame
        self.flags["graph"].set()
        while self.flags["time"] is not None and self.flags["graph"] is not None:
            # print("graphFlag.set()")

            self.flags["time"].wait()
            # print("graphFlag.wait graph end")
            if prev_frame is not self.actual_frame:
                prev_frame = self.actual_frame
                print("graph frame " + str(self.actual_frame))
                self.img_graph_frame.set_image(chunks[self.actual_frame])

    def update(self):
        self.__load_video()

        if self.clip is not None:
            self.flags["time"].set()
            self.flags["time"].clear()

            if (self.is_play and self.selected_frame_ini <= self.actual_frame < self.selected_frame_end) or self.is_one_frame:
                if self.is_one_frame:
                    self.is_one_frame = False
                else:
                    self.actual_frame += 1
                print("frame " + str(self.actual_frame))

    def play(self):
        if self.clip is not None:
            self.actual_frame = self.selected_frame_ini
            self.is_play = True

    def pause(self):
        if self.clip is not None:
            self.is_play = not self.is_play

    def one_frame_backward(self):
        if self.clip is not None:
            if self.general_frame_ini < self.actual_frame:
                self.is_play = False
                self.is_one_frame = True
                self.actual_frame -= 1

    def one_frame_forward(self):
        if self.clip is not None:
            if self.actual_frame < self.general_frame_end:
                self.is_play = False
                self.is_one_frame = True
                self.actual_frame += 1

    def select_frame_ini(self):
        if self.clip is not None:
            if self.actual_frame < self.selected_frame_end:
                self.selected_frame_ini = self.actual_frame
                print("ini selected frame {} ".format(self.actual_frame))

    def select_frame_end(self):
        if self.clip is not None:
            if self.actual_frame > self.selected_frame_ini:
                self.selected_frame_end = self.actual_frame
                print("end selected frame {} ".format(self.actual_frame))

    def export(self):
        if self.clip is not None:

            print("Saving frame_ini = {}, frame_end = {}".format(self.selected_frame_ini, self.selected_frame_end))

            _video = VideoFileClip(self.path_video)
            _fpms = _video.fps / 1000
            sub_video = _video.subclip(self.selected_frame_ini * _fpms, self.selected_frame_end * _fpms)

            export_base_path = os.path.splitext(self.path_video)[0]
            sub_video_path = export_base_path + "_edited.mp4"
            sub_video.write_videofile(filename=sub_video_path, codec="mpeg4", audio_codec='aac')
            _video.close()

            self.export_data = {
                "video_path": self.path_video,
                "video_fps": _video.fps,
                "sub_video_path": sub_video_path,
                "exported_date": datetime.now(),
                "selected_frame_ini": self.selected_frame_ini,
                "selected_frame_end": self.selected_frame_end
            }

            with open(export_base_path + "_edited_data.json", 'w') as json_file:
                json.dump(self.export_data, json_file, default=str)

    def load_export_data(self):
        sub_video_path = os.path.splitext(self.path_video)[0] + "_edited_data.json"
        if os.path.exists(sub_video_path) and os.path.isfile(sub_video_path):
            with open(sub_video_path) as json_file:
                self.export_data = json.load(json_file)
                self.selected_frame_ini = self.export_data["selected_frame_ini"]
                self.selected_frame_end = self.export_data["selected_frame_end"]
                self.exported_date = self.export_data["exported_date"]

def was_exported(video_path):
    sub_video_path = os.path.splitext(video_path)[0] + "_edited_data.json"
    return os.path.exists(sub_video_path) and os.path.isfile(sub_video_path)



