import simpleaudio as sa
import threading
import sys
import os
import subprocess
import wave
from os.path import dirname, join as join_path


class WavFile:
    """
    Class contains parameters of sound file
    """
    def __init__(self, path):
        self.wave_object = sa.WaveObject.from_wave_file(path)
        self.file_name = path
        with wave.open(path, "rb") as f:
            self.width = f.getsampwidth()
            self.channels = f.getnchannels()
            self.rate = f.getframerate()
            self.frames = f.getnframes()
            self.data = f.readframes(self.frames)
            self.duration = float(self.frames) / self.rate


def mute(func):
    def decorated(self, *args, **kwargs):
        if self._mute:
            return
        return func(self, *args, **kwargs)
    return decorated


class WavPlayer:
    """
    Class load sounds from files and play sounds
    """
    def __init__(self):

        self.sounds = dict()
        self._threads = []

        self._mute = False

        if sys.platform.startswith("linux"):
            self.play = self.__play_linux
        elif sys.platform.startswith("win"):
            import winsound
            self.winsound = winsound
            self.play = self.__play_win
        else:
            self.play = self.__play_sa

    def set_mute(self, state: bool = True):
        self._mute = state

    @property
    def mute(self):
        return self._mute

    def check_sound_available(self):
        path_to_dummy_wav = join_path(dirname(__file__), "void.wav")
        self.add_sound(path_to_dummy_wav, "epsound_test_sound_for_driver_checking")
        try:
            self.play("epsound_test_sound_for_driver_checking")
            return True
        except RuntimeError:
            return False

    def add_sound(self, file: str, name: str):
        """
        Function create WavFile-object with sound and add him to list
        :param file: filename with sound
        :param name: name of sound
        :return:
        """
        self.sounds[name] = WavFile(file)

    def stop(self):
        """
        Function stop thread with sound
        :return:
        """
        for th in self._threads:
            th.join()

    @mute
    def __play_sa(self, sound_name: str):
        """
        Function play sound in another OS
        :param sound_name: name of sound in class
        :return:
        """
        def _play():
            self.sounds[sound_name].wave_object.play()
        thread = threading.Thread(target=_play, args=())
        self._threads.append(thread)
        thread.start()

    @mute
    def __play_win(self, sound_name: str):
        """
        Function play sound on windows
        :param sound_name: name of sound in class
        :return:
        """
        self.winsound.PlaySound(self.sounds[sound_name].file_name, self.winsound.SND_NOSTOP)

    @mute
    def __play_linux(self, sound_name: str):
        """
        Function play sound on linux
        :param sound_name: name of sound in class
        :return:
        """
        proc = subprocess.Popen(['aplay', self.sounds[sound_name].file_name])
        proc.wait()
