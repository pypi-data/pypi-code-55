"""edenpy logger"""

import logging
import logging.handlers


class Logger:
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

