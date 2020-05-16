class NonexistentCoordinatesException(Exception):
    def __init__(self, error_msg, coord_name):
        self._error_msg = error_msg
        self._coord_name = coord_name

    def __str__(self):
        return "当前地点: {self._coord_name} 坐标不存在, 错误原因: {self._error_msg}".format(self=self)


class WordCloudMaskImageException(Exception):
    def __init__(self, data):
        self._data = data

    def __str__(self):
        return "错误原因: 图片无法加载或者不是一个正确的路径, 数据: {self._data}".format(self=self)
