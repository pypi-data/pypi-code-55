import os


class AdobePhotoshopStruct(object):

    def __init__(self):
        super().__init__()
        self.exe_filename = None
        self.max_root = None
        self.version = None
        self.version_str = None
        self.icon = None
        self.bit = None

    def __lt__(self, s):
        return self.version_int() < s.version_int()

    def __gt__(self, s):
        return self.version_int() > s.version_int()

    def __eq__(self, s):
        return self.version_int() == s.version_int()

    def __ge__(self, s):
        return self.version_int() >= s.version_int()

    def __le_(self, s):
        return self.version_int() <= s.version_int()

    def version_int(self):
        v = int(self.version_str.split(' ')[-1])
        return v


class AdobePhotoshop(AdobePhotoshopStruct):
    """
    Autodesk Photoshop 类
    """

    def __repr__(self):
        return '<{}_{}: \'{}\'>'.format(self.version_str, self.bit, self.__class__.__name__)

    def __init__(self):
        super().__init__()

    @classmethod
    def get_default_exe(cls):
        """
        获取ftype 关联
        :return:
        """
        data = os.popen('ftype psd').read()
        if '=' in data:
            exe = data.split('=')[1].split('" ')[0][1:]
            exe = os.path.abspath(exe)
            if os.path.exists(exe):
                return exe

    def ready_data_from_finder(self, data):
        self.exe_filename = data['path']
        self.version = data['version']
        self.version_str = data['version_string']
        self.icon = data['icon']
        self.bit = int(data['bit'])

        self.max_root = os.path.dirname(self.exe_filename)


if __name__ == '__main__':
    from cgtools.Finder import Autodesk3dsMaxFinder

    a = Autodesk3dsMaxFinder()
    a.run()

    for v in a.data:
        print(v)

    # a[2018].install_startup_script('test.ms', 'd:\\test_lib.ms', '测试菜单', uninstall = True)
