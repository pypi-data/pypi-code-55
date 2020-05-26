import pandas as pd
import numpy as np
import logging

class EmotionType:
    ANGER = "anger"
    NEUTRAL = "neutral"
    DISGUST = "disgust"
    FEAR = "fear"
    HAPPINESS = "happiness"
    SADNESS = "sadness"
    SURPRISE = "surprise"


class EmotionAnalyser:
    '''
    情绪分析器
    '''
    EMOTIONS = [EmotionType.ANGER, EmotionType.NEUTRAL,
                EmotionType.DISGUST, EmotionType.FEAR,
                EmotionType.HAPPINESS, EmotionType.SADNESS,
                EmotionType.SURPRISE]

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def merge_emotion(self, audio_emotion, frame_emotion):
        pass

    def get_emotion_global_distribution(self, emotion):
        """

        获取情绪的分布

        Args:
            emotion: [{"anger": 0.1, "neutral": 0.1, "disgust": 0.1, "fear": 0.005670338961718315, "happiness": 0.2 "sadness": 0.1, "surprise": 0.2}, ...]

        Returns:
            dict: distribution -> {'anger': 0.04678370220399322, 'neutral': 0.04147910314122111, 'disgust': 0.05076599764308418, 'fear': 0.012459961661656426, 'happiness': 0.3805726751609995, 'sadness': 0.001341534333740512, 'surprise': 0.46659702585530505}
        """

        emotion_df = self.__construct_emotion_df(emotion)
        distribution = self.__calculate_distribution(emotion_df)
        return distribution

    def get_emotion_from_video(self, video_path):
        pass

    def get_fluctuation_from_emotion(self, emotion):
        """

        获取情绪的波动

        Args:
            emotion: [{"anger": 0.1, "neutral": 0.1, "disgust": 0.1, "fear": 0.005670338961718315, "happiness": 0.2 "sadness": 0.1, "surprise": 0.2}, ...]

        Returns:
            list: fluction -> [0.2625822317841726, 0.286318327656083, 0.19226654361134174, 0.26339393328225225, 0.3021995866171042, 0.2843571171657221, ...]
        """

        emotion_df = self.__construct_emotion_df(emotion)
        distribution = self.__calculate_distribution(emotion_df)
        fluctuation = self.__calculate_fluctuation(emotion_df, distribution)
        return fluctuation

    def parse(self, emotion):
        '''
        情绪整体分析，返回情绪数据，情绪总体分布，情绪波动

        Args:
            emotion: [{"anger": 0.1, "neutral": 0.1, "disgust": 0.1, "fear": 0.005670338961718315, "happiness": 0.2 "sadness": 0.1, "surprise": 0.2}, ...]

        Returns:
            list: data ->[[2.639, 1.415, 45.941, 3.918, 34.431, 0.159, 11.497], [0.685, 18.661, ... ] ... ]  顺序为['anger', 'neutral', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']
            dict: distribution
            list: fluction
        '''

        emotion_df = self.__construct_emotion_df(emotion)
        distribution = self.__calculate_distribution(emotion_df)
        fluctuation = self.__calculate_fluctuation(emotion_df, distribution)
        return emotion_df.round(decimals=3).values.tolist(), distribution, fluctuation

    def __construct_emotion_df(self, emotion):
        self.logger.debug("construct emotion dataframes")
        emotion_df = pd.DataFrame(emotion)
        # 设置表头
        emotion_df = emotion_df[self.EMOTIONS]
        # 设置需要插值的位置
        emotion_df[emotion_df.sum(axis=1) == 0] = np.nan
        # 插值每一列中nan的数值
        emotion_df = emotion_df.interpolate(
                method='linear', limit_direction='both', axis=0)
        emotion_df = emotion_df.fillna(0)
        return emotion_df

    def __calculate_distribution(self, emotion_df):
        self.logger.debug("calculate the emotion distribution")
        each_emotion_sum = {e: sum(emotion_df[e]) for e in emotion_df.keys()}
        emotion_sum = sum(each_emotion_sum.values())
        if emotion_sum == 0:
            return {}
        return {k: v * 1.0 / emotion_sum for k, v in each_emotion_sum.items()}

    def __calculate_fluctuation(self, emotion_df, distribution):
        self.logger.debug("calculate the emotion fluction")
        if not distribution:
            return []
        fluctuation = []
        average_emotion = distribution[EmotionType.HAPPINESS] -\
                            distribution[EmotionType.SADNESS]
        for index, row in emotion_df.iterrows():
            emotion_sum = sum(row[e] for e in [EmotionType.SADNESS,
                                               EmotionType.NEUTRAL,
                                               EmotionType.HAPPINESS])
            if emotion_sum == 0:
                fluctuation.append(0)
            else:
                negative_score = row[EmotionType.SADNESS] / emotion_sum
                positive_score = row[EmotionType.HAPPINESS] / emotion_sum
                fluctuation.append(
                        (positive_score - negative_score - average_emotion) / 2)
        return fluctuation


if __name__ == "__main__":
    fake_emotion = [{'anger': 0.001, 'neutral': 0.852, 'disgust': 0.028, 'fear': 0.002,
             'happiness': 0.058, 'sadness': 0.011, 'surprise': 0.048},
            {
                'anger': 0.001, 'neutral': 0.852, 'disgust': 0.028, 'fear': 0.002, 'happiness': 0.058, 'sadness': 0.011,
                'surprise': 0.048
            }]
    ea = EmotionAnalyser()
    print(ea.EMOTIONS)
    print(ea.parse(fake_emotion))

