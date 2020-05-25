class ResultInfo(object):
    """返回结果"""

    def __init__(self,error_no=0,error_info="",data=None):

        """错误码"""
        self.error_no = error_no

        """错误信息"""
        self.error_info = error_info

        """数据"""
        self.data = data

