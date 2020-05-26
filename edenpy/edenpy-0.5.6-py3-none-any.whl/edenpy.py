"""utils for python projects"""

import os.path
import json
import logging
import logging.handlers


class logger:
    """customized logger"""

    def __init__(self):
        # logger instance 생성
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=logging.INFO)

        # formatter 생성
        formatter = logging.Formatter("[%(asctime)s][%(levelname)8s][%(filename)15s][%(lineno)4s]\t>>\t%(message)s")

        # handler 생성 (stream, file)
        streamHandler = logging.StreamHandler()
        fileHandler = logging.FileHandler("./log.log")

        # logger instance에 formatter 설정
        streamHandler.setFormatter(formatter)
        fileHandler.setFormatter(formatter)

        # logger instance에 handler 설정
        self.logger.addHandler(streamHandler)
        self.logger.addHandler(fileHandler)


def save_json(data, path):
    """

    Args:
        data: 저장 할 파일
        path: 파일 이름까지 포함하는 저장 경로

    Returns:

    """
    if os.path.isfile(path):
        with open(path) as jf:
            new_data = json.load(jf)
            new_data.extend(data)
    else:
        new_data = data

    print(new_data)
    with open(path, 'w', encoding="utf-8") as jfout:
        json.dump(new_data, jfout, indent="\t", ensure_ascii=False)


def test():
    print(847213)
