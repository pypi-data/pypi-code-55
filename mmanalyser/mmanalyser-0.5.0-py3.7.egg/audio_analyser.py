# -*- coding: utf-8 -*-
import numpy as np
from mmanalyser.utils.vad import vad_robust
from pyAudioAnalysis import audioTrainTest as aT
import logging
import os
import subprocess
import shutil


class AudioAnalyser:
    '''
    音频分析器

    '''
    def __init__(self, rationality_service_url=None):
        self.logger = logging.getLogger(self.__class__.__name__)

    def is_valid_audio(self, audio_path, human_voice_length=4):
        pred = self.is_human_voice(audio_path)
        return pred > 0.5, pred

    def is_human_voice(self, audio_path, human_voice_length=1, mode=0):
        pred = 0
        if mode == 0:
            paths, voiced_range, voiced_duration, duration = vad_robust(
                audio_path, span=3, chunk_dir='temp/')
            if voiced_duration >= human_voice_length:
                pred = float(
                    np.mean(
                        [self.is_human_voice_snippet(x) for x in paths[1:]]))
        elif mode == 1:
            paths, voiced_range, voiced_duration, duration = vad_robust(
                audio_path, chunk_dir='temp/')
            if voiced_duration >= human_voice_length:
                haha = np.array([[idx, x[0][1] - x[0][0]]
                                for idx, x in enumerate(voiced_range)
                                if x[0][1] - x[0][0] > 1])
                if len(haha) > 0:
                    haha[:, 1] = haha[:, 1] / np.sum(haha[:, 1])
                    pred = sum([
                        self.is_human_voice_snippet(paths[1 + int(idx)]) * ratio
                        for idx, ratio in haha
                    ])

        chunk_dir = os.path.join('temp/', os.path.basename(audio_path)[:-4])
        shutil.rmtree(chunk_dir)
        return pred

    def is_human_voice_snippet(self, audio_path):
        pred = aT.file_classification(
            audio_path,
            os.path.join(os.path.dirname(os.path.dirname(__file__)),
                         'mmanalyser', 'data', "gbdt"),
            "gradientboosting")[1][0]
        return pred

    def delete_silence_snippet(self, audio_path, chunk_dir='temp/'):
        if chunk_dir is None:
            chunk_dir = 'temp/'
        return vad_robust(audio_path, chunk_dir=chunk_dir)

    def convert_to_wav(self,
                       source_path,
                       desc_path,
                       channel=1,
                       sample_rate=16000):
        cmd = [
            "ffmpeg", "-i", f"{source_path}", "-f", "wav", "-ar",
            str(sample_rate), "-ac",
            str(channel), f"{desc_path}"
        ]
        if os.path.exists(desc_path):
            os.remove(desc_path)
        self.logger.info(' '.join(cmd))
        obj = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
        status_code = obj.wait()
        return status_code
