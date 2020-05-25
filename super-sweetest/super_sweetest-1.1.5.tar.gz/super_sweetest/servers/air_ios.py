# coding=utf-8

# @Time: 2020/4/10 16:42
# @Auther: liyubin


from airtest.core.api import *
from poco.drivers.ios import iosPoco
from super_sweetest.servers.ios_server import kill_ios_tagent_server, run_ios_tagent_server
from super_sweetest.servers.ios_server import get_server_url

########################################
# from airtest.core.settings import Settings

# 全局伐值

# Settings.THRESHOLD_STRICT = 0.6  # assert_exists语句的默认阈值，一般比THRESHOLD更高一些
# Settings.THRESHOLD = 0.6  # 其他语句的伐值
# Settings.OPDELAY = 1  # 每一步操作后等待1秒再进行下一步操作
# Settings.FIND_TIMEOUT = 10  # 图像查找超时时间
# Settings.CVSTRATEGY = ["surf", "tpl", "brisk"]  # 修改图片识别算法顺序，只要成功匹配任意一个符合设定阙值的结果，程序就会认为识别成功

########################################


"""
airtest ios  服务
"""


class AirIos():

    def setup_air_ios(self, device_name, app_package, desired_caps):
        """
        connect_device airtest， init poco
        """

        auto_setup(__file__)

        # 获取配置
        iostagen_file = desired_caps.get('iostagen_file', '未配置')
        platform = desired_caps.get('platform', '未配置')

        # 服务启动
        self.setup_server(iostagen_file, platform, device_name)

        # 获取server_url
        server_url = get_server_url(device_name)
        if server_url == 'retry server':
            self.setup_server(iostagen_file, platform, device_name)
            server_url = get_server_url(device_name)

        # 通过ADB连接本地Android设备
        # init_device("Android")
        # 或者使用connect_device函数
        connect_device("ios:///" + server_url)

        # poco服务,先连接设备再初始化
        poco = iosPoco()

        start_app(app_package)

        sleep(8)
        return poco

    @staticmethod
    def setup_server(iostagen_file, platform, devicename):
        """airtest ios前置条件server"""
        kill_ios_tagent_server(devicename)
        run_ios_tagent_server(iostagen_file, platform, devicename)

    @staticmethod
    def teardown_air_ios(g):
        """关闭app，停止poco实例"""
        stop_app(g.appPackage)
        kill_ios_tagent_server(g.deviceName)

# if __name__ == '__main__':
#     desired_caps = {'iostagen_file_': '/Users/li/projects/ios_project/iOS-Tagent11d',
#                     'platform': 'iOS Simulator',
#                     }
#     iostagen_file_ = '/Users/li/projects/ios_project/iOS-Tagent11d'
#     platform_ = 'iOS Simulator'  # 模拟器
#     deviceName_ = 'iPhone 11'
#     app_package = 'com.apple.Preferences'
#
#     air = AirIos()
#     air.setup_air_ios(iostagen_file_, platform_, desired_caps)
