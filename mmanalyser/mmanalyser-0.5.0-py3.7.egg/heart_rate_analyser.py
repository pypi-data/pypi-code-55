from mmanalyser import config
import numpy as np
import logging


class HeartRateAnalyser:
    '''
    心率分析器
    '''
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_bpm_from_heart_rate(self, heart_rate):
        '''

        Args:
            heart_rate: [[70, 1000.0], [75, 2000.0], ...]

        Returns:
            list: [70, 71, ...] 平滑过的心率波动
        '''
        # 整合心率到每秒，考虑到帧率并不能与毫秒对齐
        count = 1
        bpm_res = []
        # 对心率结果平均duration作一次平均
        duration = config.heart_rate_duration
        bpm_tmps = []
        for x in heart_rate:
            if duration * count > x[1] >= duration * (count - 1):
                bpm_tmps.append(x[0])
            else:
                bpm_res.append(np.mean(bpm_tmps))
                bpm_tmps = [x[0]]
                count += 1
        if len(bpm_tmps) > 0:
            bpm_res.append(np.mean(bpm_tmps))
        length = len(bpm_res)
        bpm = []
        windows = config.heart_rate_windows  # 平滑窗口
        if windows > 1:
            for idx in range(length):
                if idx - windows < 0:
                    value = np.mean(bpm_res[:idx + windows + 1])
                elif idx + windows > length:
                    value = np.mean(bpm_res[idx - windows:])
                else:
                    value = np.mean(bpm_res[idx - windows:idx + windows + 1])
                bpm.append(value)
        else:
            bpm = bpm_res
        return bpm
