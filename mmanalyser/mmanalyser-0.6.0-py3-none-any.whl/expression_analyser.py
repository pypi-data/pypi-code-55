import re
import numpy as np
from pydub import AudioSegment
from pypinyin import pinyin as get_pinyin, Style
from mmanalyser.utils.wer import wer
from mmanalyser.utils.number_to_chinese import number_to_chinese
from mmanalyser.utils.vad import vad_robust
from mmanalyser import config
import logging

WORD_SEP = '#'
AUDIO_START_TIME = 500


class ExpressionAnalyser:
    '''
    表达能力分析器

    asr数据格式：{"pause_detection": [[3280, 3922], [7781, 8688]], "text_corrected":  [], "text":  [[[0, 1170], "领导你好，"],
                                     [[8940, 12250], "我在嘉兴，"], [[12250, 13490], "有两家造纸厂，"]]}
    '''
    def __init__(self, rationality_service_url=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ntc = number_to_chinese()
        self.middle_value = dict()

    def get_expression_score(self, asr, pinyin, audio_path, use_pinyin=False):
        """
        获取表达能力分数

        Args:
            asr: asr结果
            audio_path:  音频地址

        Returns:
             dict: {
            'talk_speed': float,        // 语速
            'audio_clear': bool,        //声音是否清晰
            'mandarin_score': float,    //普通话标准程度
            'expression_score': float,  //表达能力分数
            }
        """
        self.middle_value['path'] = audio_path
        raw_text = ''.join([x[1] for x in asr['text']])
        recognition_duration, pause_moment = self.__get_duration_information(
            audio_path)
        text, text_length, particle_count, repeat_one_count, ranhou_count = self.__disfluency_detection(
            raw_text, pinyin, use_pinyin)
        mandarin_score = self.__parse_mandarin_score(text, pinyin)
        talk_speed = self.__get_talk_speed(text_length, recognition_duration)
        audio_clear = self.__is_audio_clear(audio_path, text_length,
                                            recognition_duration,
                                            mandarin_score)
        express_score = self.__parse_expression_score(
            audio_clear, text_length, pause_moment, recognition_duration,
            particle_count, mandarin_score, repeat_one_count, ranhou_count)
        self.middle_value.update({
            'talk_speed': talk_speed,
            'audio_clear': audio_clear,
            'mandarin_score': mandarin_score,
            'expression_score': express_score,
        })
        return {
            'talk_speed': talk_speed,
            'audio_clear': audio_clear,
            'mandarin_score': mandarin_score,
            'expression_score': express_score,
        }

    def get_talk_speed(self, asr):
        '''
        获取语速指标

        Args:
            asr: asr 结果
        Returns:
           float: 语速
        '''
        raw_text = ''.join([x[1] for x in asr['text']])
        recognition_duration, pause_moment = \
            self.__get_duration_information(asr)
        text, text_length, particle_count, repeat_one_count, ranhou_count = \
            self.__disfluency_detection(raw_text)
        talk_speed = self.__get_talk_speed(text_length, recognition_duration)
        return talk_speed

    def get_mandarin_score(self, asr, pinyin):
        '''
        获取普通话标准程度

        Args:
            asr: asr结果
            pinyin: 拼音识别结果（"wo2 ai2 ni3"）
        Returns:
            float: 普通话标准程度
        '''

        raw_text = ''.join([x[1] for x in asr['text']])
        text = re.sub(config.text_clean, '', raw_text)
        return self.__parse_mandarin_score(text, pinyin)

    def get_audio_clear(self, asr, audio_path, pinyin):
        '''
        获取声音是否清晰

        Args:
            asr: asr结果
            audio_path: 音频地址

        Returns:
            bool: 清晰返回true 不清晰返回false
        '''
        raw_text = ''.join([x[1] for x in asr['text']])
        recognition_duration, pause_moment = \
            self.__get_duration_information(asr)
        text, text_length, particle_count, repeat_one_count, ranhou_count = \
            self.__disfluency_detection(raw_text)
        mandarin_score = self.__parse_mandarin_score(text)
        audio_clear = self.__is_audio_clear(audio_path, text_length,
                                            recognition_duration,
                                            mandarin_score)
        return audio_clear

    def __get_talk_speed(self, text_length, recognition_duration):
        self.logger.debug("get talk speed")
        return text_length / recognition_duration

    def __is_audio_clear(self, audio_path, length, recognition_duration,
                         mandarin_score):
        self.logger.debug("get audio clear")
        flag = (
            mandarin_score != 0 and recognition_duration > 0 and
            (length / recognition_duration > 0.75 or
             (length / recognition_duration < 0.75 and mandarin_score > 50)))
        if audio_path is not None:
            dBFS_var, dBFS_mean = self.__get_dBFS_information(audio_path)
            return bool(dBFS_mean < config.voice_dBFS_human_max
                        and dBFS_var > config.voice_dBFS_human_var_min
                        and flag)
        else:
            return flag

    def __parse_mandarin_score(self, text, pinyin):
        self.logger.debug("parse mandarin score")
        if pinyin is None or text is None:
            return 70

        def func(x):
            #return x
            if x > 1.2:
                return 0.15 / x
            elif x < 0.4:
                return 0.1 * (0.4 - x) + 0.95
            else:
                return (1.2 - x) / 0.8 * 0.85 + 0.10

        text = self.ntc.parse(text)
        text = ' '.join(
            [x[0] for x in get_pinyin(str(text), style=Style.TONE3)])
        return func(wer(text, pinyin)) * 100

    def __parse_expression_score(self, audio_clear, text_length, pause_moment,
                                 recognition_duration, particle_count,
                                 mandarin_score, repeat_one_count,
                                 ranhou_count):
        self.logger.debug("get expression score")
        if not audio_clear:
            return 0

        if len(pause_moment) == 0:
            recognition_duration_per_pause_count = config.voice_recognition_duration_per_pause_count_max
        else:
            recognition_duration_per_pause_count = text_length / \
                len(pause_moment)

        recognition_duration_per_pause_count_score = self.__min_max_scaler(
            recognition_duration_per_pause_count,
            config.voice_recognition_duration_per_pause_count_min,
            config.voice_recognition_duration_per_pause_count_max)
        pause_duration_ratio = sum(
            pause_moment
        ) / recognition_duration if recognition_duration > 0 else 1
        pause_duration_ratio_score = self.__min_max_scaler(
            pause_duration_ratio,
            config.voice_pause_duration_ratio_min,
            config.voice_pause_duration_ratio_max,
            negative=True)

        # 语气词 0~1分
        if particle_count == 0:
            length_per_count = config.voice_length_per_count_max
        else:
            length_per_count = text_length / particle_count
        length_per_count_score = self.__min_max_scaler(
            length_per_count, config.voice_length_per_count_min,
            config.voice_length_per_count_max)

        ranhou_count_per_length = ranhou_count / text_length
        ranhou_count_per_length_score = self.__min_max_scaler(
            ranhou_count_per_length, 0.02, 0.06)

        repeat_one_count_per_length = repeat_one_count / text_length
        repeat_one_count_score = self.__min_max_scaler(
            repeat_one_count_per_length,
            config.voice_repeat_one_count_min,
            config.voice_repeat_one_count_max,
            negative=True)
        decay_factor = 0.8 if pause_duration_ratio_score < 0.1 or \
            recognition_duration_per_pause_count_score < 0.1 or \
            length_per_count_score < 0.1 or \
            repeat_one_count_score < 0.1 else 1
        num = int(pause_duration_ratio_score > 0.9) + int(
            recognition_duration_per_pause_count_score > 0.9) + int(
                length_per_count_score > 0.9) + int(
                    repeat_one_count_score > 0.9)
        self.middle_value.update(
            dict(recognition_duration_per_pause_count=
                 recognition_duration_per_pause_count,
                 pause_duration_ratio=pause_duration_ratio,
                 ranhou_count_per_length=ranhou_count_per_length,
                 length_per_count=length_per_count,
                 repeat_one_count_per_length=repeat_one_count_per_length))

        if text_length < 20:
            text_length_decay_factor = text_length / 20
        else:
            text_length_decay_factor = 1

        return (0.5 * pause_duration_ratio_score +
                0.5 * recognition_duration_per_pause_count_score +
                1.5 * length_per_count_score +
                1.5 * repeat_one_count_score) * decay_factor * (
                    0.85 + 0.1 * mandarin_score /
                    100) * 20 * text_length_decay_factor + 5 * num - ranhou_count_per_length_score * 10

    def __get_duration_information(self, audio_path):
        result = vad_robust(audio_path)[1]
        recognition_duration = sum([x[1] - x[0] for x in result])
        # 停顿
        moment = []
        for x in result:
            moment.append(x[0])
            moment.append(x[1])
        pause_moment = []
        for x in range(2, len(moment), 2):
            duration = (moment[x] - moment[x - 1])
            if duration > 0.5:
                pause_moment.append(duration)
        self.middle_value['recognition_duration'] = recognition_duration
        self.middle_value['pause_moment'] = pause_moment
        return recognition_duration, pause_moment

    def __disfluency_detection(self, text, pinyin, use_pinyin=False):
        text = re.sub(config.text_clean, '', text)
        text = re.sub('[a-zA-Z]', '', text)
        if not use_pinyin:
            # 语气词
            particle_count = len(
                re.findall(config.voice_modal_particles_pattern, text))
            # 文本清理
            repeat_one_count = len(self.__get_repeat_record_by_offset(text, 1))
            ranhou_count = len(re.findall('然后', text))
            text_length = len(text)
        else:
            # 语气词
            particle_count = len(
                re.findall(config.voice_modal_particles_pattern_pinyin,
                           ' ' + pinyin + ' '))
            # 文本清理
            repeat_one_count = len(
                self.__get_repeat_record_by_offset(pinyin, 1))
            ranhou_count = len(re.findall(' ran2 hou4 ', pinyin))
            text_length = len(pinyin.split())

        self.middle_value['text_length'] = text_length
        self.middle_value['text'] = text
        self.middle_value['ranhou_count'] = ranhou_count
        self.middle_value['repeat_one_count'] = repeat_one_count
        self.middle_value['particle_count'] = particle_count
        return text, text_length, particle_count, repeat_one_count, ranhou_count

    def __get_dBFS_information(self, audio):
        sound = AudioSegment.from_file(audio, "mp3")
        dBFS = []
        for x in range(AUDIO_START_TIME, len(sound),
                       config.voice_dBFS_sample_interval):
            dbfs = sound[x:x + config.voice_dBFS_sample_interval].dBFS
            if dbfs != float("-inf"):
                dBFS.append(dbfs)
        return np.var(dBFS), np.mean(dBFS)

    def __min_max_scaler(self, value, min_value, max_value, negative=False):
        score = 0
        if value > max_value:
            score = 1
        elif value > min_value:
            diff = value - min_value
            score += diff / (max_value - min_value)
        return score if not negative else 1 - score

    def __get_repeat_record_by_offset(self, text, offset=1):
        assert offset > 0
        length = len(text)
        repeat_record = []
        word = text[0:offset] if length > 0 else ''
        i = offset * 2
        count = 1
        while i < length + 1:
            if word == text[i - offset:i]:
                count += 1
            else:
                if count > 1:
                    if word + word not in ['勉勉', '强强', '谢谢']:
                        repeat_record.append(count)
                i = i - offset + 1
                count = 1
                word = text[i - offset:i]
            i = i + offset
        if count > 1:
            if word + word not in ['勉勉', '强强', '谢谢']:
                repeat_record.append(count)
        return repeat_record

    def __get_repeat_record_pinyin_by_offset(pinyin, offset=1):
        assert offset > 0
        data = pinyin.split(' ')
        pinyin2idx = {y: chr(x) for x, y in enumerate(data)}
        # idx2pinyin = {y:x for x, y in pinyin2idx.items()}
        text = ''.join([pinyin2idx[x] for x in data])
        length = len(text)
        repeat_record = []
        word = text[0:offset] if length > 0 else ''
        i = offset * 2
        count = 1
        while i < length + 1:
            if word == text[i - offset:i]:
                count += 1
            else:
                if count > 1:
                    repeat_record.append(count)
                i = i - offset + 1
                count = 1
                word = text[i - offset:i]
            i = i + offset
        if count > 1:
            repeat_record.append(count)
        return repeat_record

if __name__ == '__main__':
    ea = ExpressionAnalyser()
    fake_asr = {
        "pause_detection": [[3280, 3922], [7781, 8688]],  # 停顿检测结果
        "text": [[[0, 1170], "领导你好，"], [[1170, 2370], "我叫秦嘉涵，"],
                 [[2370, 5530], "今年26岁，"], [[5530, 8040], "是浙江龙游人，"],
                 [[8040, 8940], "我，"], [[8940, 12250], "我在龙游，"],
                 [[12250, 13490], "有两家造纸厂，"], [[13490, 19330], "有4年的维修工禁令。"]]
    }
    fake_pinyin = ' '.join(
        [x[0] for x in get_pinyin("领导你好", style=Style.TONE3)])
    print(ea.get_expression_score(asr=fake_asr,
                                pinyin=fake_pinyin,
                                audio_path='temp/10.wav'))
    print(ea.middle_value)
    print(
        ea.get_expression_score(asr=fake_asr,
                                pinyin=fake_pinyin,
                                audio_path='temp/10.wav',
                                use_pinyin=True))
    print(ea.middle_value)
    print(ea.get_mandarin_score(asr=fake_asr, pinyin=fake_pinyin))
