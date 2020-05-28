import numpy as np
from mmanalyser import config
from mmanalyser.utils.suffix_remover import suffix_remover
import logging


class FluctuationDetector:
    '''
    波动检测器
    '''
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_abnormal_fluctuation_range_from_heart_rate(self, heart_rate_infos):
        '''
        从心率信息中抽取异常波动时间范围

        Args:
            heart_rate_infos: [[70, 1000.0], [75, 2000.0], ...]

        Returns:
            list: [start_time, end_time]
        '''
        # 取第10s到第15s区间的心率均值作为基准
        bpm_baseline = np.mean(
            [x[0] for x in heart_rate_infos if 10000 <= x[1] <= 15000])
        if np.isnan(bpm_baseline):
            bpm_baseline = 70.0
        # 找出超过基准心率 25% 以上，且波动最大的区间
        thresh = bpm_baseline * 1.25
        significant_info = [0, 0, 0]
        sig = False
        accum_bpm = 0
        count = 0
        for x in heart_rate_infos:
            if x[0] > thresh:
                accum_bpm += x[0]
                count += 1
                if not sig:
                    start = x[1]
                    sig = True
            elif x[0] <= thresh and sig:
                end = x[1]
                sig = False
                mean_bpm = accum_bpm / float(count)
                accum_bpm = 0
                count = 0
                # 持续时间超过 1s 才记录
                if end - start > 1000 and mean_bpm > significant_info[2]:
                    significant_info = [start, end, mean_bpm]
        return significant_info[:2]

    def get_abnormal_fluctuation_range_from_emotion_fluction(self, emotion_fluctuation):
        '''
        从情绪波动信息中抽取异常波动时间范围

        Args:
            emotion_fluctuation: [0.2625822317841726, 0.286318327656083, 0.19226654361134174, 0.26339393328225225, 0.3021995866171042, 0.2843571171657221, ...]

        Returns:
            list: [start_time, end_time]

        '''
        fluctuation_abs = list(map(abs, emotion_fluctuation))
        max_val = max(fluctuation_abs)
        emotion_change_threshold = 0.9
        if max_val > emotion_change_threshold:
            start = fluctuation_abs.index(max_val)
            return (start * config.KEY_FRAME_INTERVAL * 1000,
                    (start + 1) * config.KEY_FRAME_INTERVAL * 1000)
        return None

    def get_text_from_emotion_abnormal_fluction(self, text_with_timestamp, emotion_fluctuation):
        '''
        结合带时间戳的文本抽取当情绪波动异常时的文本

        Args:
            text_with_timestamp: [[[[0, 1170], "领导你好，"], [[1170, 2370], "我叫，"]], ...]
            emotion_fluctuation: [0.2625822317841726, 0.286318327656083, 0.19226654361134174, 0.26339393328225225, 0.3021995866171042, 0.2843571171657221, ...]

        Returns
            str: "abnormal_text"
        '''
        emotion_range = self.get_abnormal_fluctuation_range_from_emotion_fluction(emotion_fluctuation)
        return self.__get_text_from_range(text_with_timestamp, emotion_range)

    def get_text_from_heart_rate_abnormal_fluction(self, text_with_timestamp, heart_rate):
        '''
        结合带时间戳的文本抽取心率波动异常时的文本

        Args:
            text_with_timestamp: [[[[0, 1170], "领导你好，"], [[1170, 2370], "我叫，"]], ...]
            heart_rate: [[70, 1000.0], [75, 2000.0], ...]

        Returns:
            str: "abnormal_text"
        '''
        heart_rate_range = self.get_abnormal_fluctuation_range_from_heart_rate(heart_rate)
        return self.__get_text_from_range(text_with_timestamp, heart_rate_range)

    def __get_text_from_range(self, text_with_timestamp, range):
        abnormal_text = ''
        if text_with_timestamp and range:
            for r, text in text_with_timestamp:
                if self.__overlap(r, range):
                    abnormal_text += text
        return suffix_remover.remove_suffix(abnormal_text)

    def __overlap(self, r1, r2):
        return r2[0] <= r1[0] <= r2[1] or r2[0] <= r1[1] <= r2[1] or \
               r1[0] <= r2[0] <= r1[1] or r1[0] <= r2[1] <= r1[1]


if __name__ == '__main__':
    fake_heart_rate_fluction = [72.57492507492508, 92.03153144697094, 78.93288496016338, 84.63336143314451, 87.28089096665917, 86.75675675675674, 97.29729729729729, 104.59459459459457, 76.2162162162162, 60.81081081081082, 60.81081081081082, 60.81081081081082, 60.81081081081082, 60.81081081081082, 77.02702702702703, 80.27027027027025, 72.97297297297295, 67.2972972972973, 94.86486486486487, 81.08108108108108]
    text = [[[0, 1170], "领导你好，"], [[1170, 2370], "我叫，"], [[2370, 5530], "今年26岁，"], [[5530, 8040], "是浙江人，"], [[8040, 8940], "我，"], [[8940, 12250], "我在龙游，"], [[12250, 13490], "有两家造纸厂，"], [[13490, 19330], "有4年的维修工禁令。"]]
    fa = FluctuationDetector()
    print(fa.get_text_from_emotion_abnormal_fluction(text_with_timestamp=text, emotion_fluctuation=fake_emotion_fluction))

