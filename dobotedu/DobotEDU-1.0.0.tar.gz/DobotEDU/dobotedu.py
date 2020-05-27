from aip import AipSpeech
from aip import AipNlp
from aip import AipImageClassify
from aip import AipOcr
from aip import AipFace
from DobotRPC import DobotlinkAdapter, RPCClient
import cv2
import sounddevice as sd
import soundfile as sf
import requests


class DobotEDU(object):
    def __init__(self, user_name: str, school_key: str):
        address = f"http://49.235.112.128:8052/{user_name}/{school_key}"
        json_result = eval(requests.get(address).content.decode())
        API_ID = f'{json_result[0]}'
        API_KEY = f'{json_result[1]}'
        SECRET_KEY = f'{json_result[2]}'

        api_id = API_ID
        api_key = API_KEY
        secret_key = SECRET_KEY

        self.__speech = AipSpeech(api_id, api_key, secret_key)
        self.__nlp = AipNlp(api_id, api_key, secret_key)
        self.__image_classify = AipImageClassify(api_id, api_key, secret_key)
        self.__ocr = AipOcr(api_id, api_key, secret_key)
        self.__face = AipFace(api_id, api_key, secret_key)

        self.__dobotlink = DobotlinkAdapter(RPCClient(), is_sync=True)

    @property
    def dobotlink(self):
        return self.__dobotlink

    # @property
    # def magician_lite(self):
    #     return self.__dobotlink.MagicianLite

    # @property
    # def magic_box(self):
    #     return self.__dobotlink.MagicBox

    @property
    def speech(self):
        return self.__speech

    @property
    def nlp(self):
        return self.__nlp

    @property
    def image_classify(self):
        return self.__mage_classify

    @property
    def ocr(self):
        return self.__ocr

    @property
    def face(self):
        return self.__face


# 待课程开发结束再加

    def get_file_content(self, filePath):  # 读取照片文件

        with open(filePath, 'rb') as fp:
            return fp.read()

    def get_image(self, filePath, count_down):  # count_down为拍照时间
        cap = cv2.VideoCapture(0)  # 用摄像头拍照
        t = count_down * 1000
        cnt = count_down
        # print("拍照倒计时....")
        while True:
            ret, frame = cap.read()  # 读取摄像头拍照的图片
            frame = cv2.flip(frame, 1)  # 左右翻转摄像头获取的照片
            cv2.imshow("video", frame)  # 显示照片
            c = cv2.waitKey(1)  # 显示的帧数
            if c == 27:
                break
            if t == 0:
                cv2.imwrite(filePath, frame)
                return
            if t % 1000 == 0:
                print(cnt)
                cnt = cnt - 1
            t = t - 20

    def record(self, filename, count_down):

        RATE = 16000  # 采样率
        RECORD_SECONDS = count_down  # 录制时长Duration of recording
        print("录制开始...")
        myrecording = sd.rec(int(RECORD_SECONDS * RATE),
                             samplerate=RATE,
                             channels=1)
        sd.wait()  # 等到录制结束
        print("录制结束...")
        sf.write(filename, myrecording, RATE, subtype='PCM_16')
