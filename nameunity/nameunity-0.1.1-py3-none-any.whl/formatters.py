# Author: LucasD11 <yuanzhendai@gmail>

import datetime


class UnknownFormat(Exception):
    pass


class Formatter:
    FORMAT = "%Y-%m-%d %H:%M:%S"
    def format(self, s):
        try:
            return self._handle(s.lower())
        except:
            raise UnknownFormat

    def _handle(self, s):
        return datetime.datetime.strptime(s, self.FORMAT)


class Formatter1(Formatter):
    "Formatter for files from Huawei P9"
    FORMAT = "img_%Y%m%d_%H%M%S.jpg"


class Formatter11(Formatter):
    "Formatter for files from Huawei P9"
    FORMAT = "img_%Y%m%d_%H%M%S_1.jpg"


class Formatter12(Formatter):
    "Formatter for files from Huawei P9"
    FORMAT = "img_%Y%m%d_%H%M%S_2.jpg"


class Formatter13(Formatter):
    "Formatter for files from Huawei P9"
    FORMAT = "vid_%Y%m%d_%H%M%S.mp4"


class Formatter2(Formatter):
    "Formatter for files from IPhone"
    FORMAT = "%Y-%m-%d %H.%M.%S.jpg"


class Formatter21(Formatter):
    "Formatter for files from IPhone"
    FORMAT = "%Y-%m-%d %H.%M.%S.png"


class Formatter22(Formatter):
    "Formatter for files from IPhone"
    FORMAT = "%Y-%m-%d %H.%M.%S.mov"


class Formatter23(Formatter):
    "Formatter for files from IPhone"
    FORMAT = "%Y-%m-%d %H.%M.%S-1.jpg"


class Formatter24(Formatter):
    "Formatter for files from IPhone"
    FORMAT = "%Y-%m-%d %H.%M.%S-1.png"



FORMATTER_CLASSES = [
    Formatter1, Formatter11, Formatter12, Formatter13,
    Formatter2, Formatter21, Formatter22, Formatter23, Formatter24
]
