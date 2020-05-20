import sounddevice
import pydub
import time
import numpy
import queue

class audio():
    def __init__(self):
        self.samples = None
        self.now = {}
        self.now.update(place=0)
        self.now.update(path="")
    def openfile(self, filepath):
        if ".mp3" in filepath:
            self.segment = pydub.AudioSegment.from_file(filepath,codec="mp3")
        elif ".wav" in filepath:
            self.segment = pydub.AudioSegment.from_file(filepath,codec="wav")
        elif ".mp4" in filepath:
            self.segment = pydub.AudioSegment.from_file(filepath)
        else:
            self.segment = pydub.AudioSegment.from_file(filepath)
        if self.now["path"] != filepath:
            self.samples = None
        self.now.update(place=0)
        self.now.update(path=filepath)
    def play(self, place=0):
        if type(self.samples) == type(None):
            if self.segment.channels != 1:
                self.samples = numpy.array(self.segment.get_array_of_samples().tolist(),dtype="int16").reshape(-1,2)
            else:
                self.samples = numpy.array(self.segment.get_array_of_samples().tolist(),dtype='int16')
            sounddevice.play(self.samples,self.segment.frame_rate)
        else:
            self.goto(place)
        self.long = len(self.samples)
        self.player = sounddevice.get_stream()
    def stop(self):
        sounddevice.stop()
    def goto(self, place):
        sounddevice.stop()
        self.player = sounddevice.play(self.samples[place*self.segment.frame_rate:-1],self.segment.frame_rate)
    def goto(self, place):
        sounddevice.stop()
        self.player = sounddevice.play(self.samples[place:-1],self.segment.frame_rate)
    def get_file_info(self,key=None):
        if key == None:
            return {}.update([("channel",self.segment.channels),("frame_rate",self.segment.frame_rate),("duration",self.segment.duration_second)])
        elif key == "channel":
            return self.segment.channels
        elif key == "frame_rate":
            return self.segment.frame_rate
        elif key == "duration_second":
            return self.segment.duration_second
        elif key == "duration_frame":
            return self.long
        else:
            return None
    def get_player():
        return self.player
    def get_status():
        return sounddevice.get_status()

def get_devicelist():
    return sounddevice.query_devices()
def get_apilist():
    return sounddevice.query_hostapis()
def get_status():
    return sounddevice.get_status()
