# -*- coding: utf-8 -*- #
"""
分析扫描软件的位置版本图标等信息
注意32和64 KEY 都要扫描

"""
import os
import winreg
import tempfile

import win32ui
import win32file
import win32api
import win32gui
from win32con import *


class IconBase(object):

    def __init__(self):
        super(IconBase, self).__init__()
        self.search_path_lst = []

    def set_search_lst(self, data):
        self.search_path_lst = data
        self.get_app_icon = self.get_app_icon_by_search

    def extract_from_file(self, filename):
        """
        提取图标从文件中 一般是exe ico
        :param filename:
        :return:
        """
        large, small = win32gui.ExtractIconEx(filename, 0)
        win32gui.DestroyIcon(small[0])
        ico_x = 32
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_x)
        hdc = hdc.CreateCompatibleDC()

        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), large[0])

        temp_png_filename = tempfile.mktemp(suffix='.png')

        from PIL import Image
        bmpstr = hbmp.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGBA',
            (32, 32),
            bmpstr, 'raw', 'BGRA', 0, 1
        )

        img.save(temp_png_filename)
        return temp_png_filename

    def get_app_icon_by_search(self, root, filename):
        for a in self.search_path_lst:
            if os.path.exists(a.format(root)):
                filename = a.format(root)
                return {'large': filename, 'small': filename}


class FindBase(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_inst'):
            cls._inst = super(FindBase, cls).__new__(cls, *args, **kwargs)
            cls._inst.init()
        return cls._inst

    def init(self):
        self.runed = False
        self.data = []

    def get_data(self):
        return self.data

    def get_data_by_version(self, version, bit):
        for a in self.data:
            if str(version) in a.version_str and a.bit == bit:
                return a

    def find(self):
        pass

    def run(self):
        if self.runed:
            return

        self.find()
        self.runed = True

    def find_value(self, key_path, found_lst, flag=KEY_WOW64_64KEY, value_name='Installdir', key_name=None,
                   spcae=winreg.HKEY_LOCAL_MACHINE):

        if key_name:
            if os.path.basename(key_path) == key_name:
                open_key = winreg.OpenKey(spcae, key_path, 0, KEY_ALL_ACCESS | flag)
                data = win32api.RegQueryValue(open_key, '')
                if data:
                    found_lst.append(data)

        try:
            open_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, KEY_ALL_ACCESS | flag)
        except:
            return

        try:
            data = win32api.RegQueryValueEx(open_key, value_name)
            if data:
                found_lst.append(data[0])
        except:
            pass

        countkey = winreg.QueryInfoKey(open_key)[0]
        for i in range(int(countkey)):
            name = winreg.EnumKey(open_key, i)
            key_index = '\\'.join((key_path, name))
            self.find_value(key_index, found_lst, flag, value_name, key_name)

        return found_lst

    def get_app_version(self, file_name):
        try:
            info = win32api.GetFileVersionInfo(file_name, os.sep)

            ms = info['FileVersionMS']
            ls = info['FileVersionLS']
            version = '%d.%d.%d.%04d' % (
                win32api.HIWORD(ms),
                win32api.LOWORD(ms),
                win32api.HIWORD(ls),
                win32api.LOWORD(ls))
            return version

        except BaseException as e:
            return 0

    def get_app_bit(self, filename):
        try:
            type = win32file.GetBinaryType(filename)
            if type == 0:
                return "32"
            elif type == 6:
                return "64"
        except BaseException as e:
            return '?'

    def get_app_icon(self, root, filename, found_lst=None):
        obj = IconBase()
        if found_lst:
            obj.set_search_lst(found_lst)

        data = obj.get_app_icon(root, filename)
        return data


class Autodesk3dsMaxFinder(FindBase):
    """
    调用run方法开始扫描全部安装max
    """

    def __str__(self):
        return 'Autodesk 3dsmax'

    def __getitem__(self, version, bit=64):
        return self.get_data_by_version(version, bit)

    def find(self):
        unkey = []

        icon_found_path = (
            '{}UI/Icons/icon_main.ico',
            '{}ui/Icons/ATS/atsscene.ico',
            '{}UI_ln/Icons/ATS/ATSScene.ico',
        )
        # find by os env
        for env_name in os.environ:
            if 'ADSK_3DSMAX' in env_name:
                root = os.environ[env_name]
                full_path = os.path.join(root, '3dsmax.exe')
                if os.path.exists(full_path):
                    bit, version = self.get_app_bit(full_path), self.get_app_version(full_path)
                    version_str = str(2000 + (int(version.split('.')[0]) - 2))
                    if int(version.split('.')[0]) < 10:
                        version_str = str(('.'.join(version.split('.')[:2])))

                    icon = self.get_app_icon(root, full_path, icon_found_path)

                    user_path = os.environ["LOCALAPPDATA"]
                    max_local_folder = os.path.join(user_path, 'Autodesk\\3dsMax',
                                                    '{} - {}bit'.format(version_str, bit))

                    max_data = {'path': full_path,
                                'local_path': max_local_folder,
                                'bit': bit,
                                'icon': icon,
                                'version': int(version.replace('.', '')),
                                'version_string': '3dsmax {}'.format(version_str)
                                }

                    from cgtools.Autodesk3dsmax import Autodesk3dsmax
                    max_obj = Autodesk3dsmax()
                    max_obj.ready_data_from_finder(max_data)
                    if full_path not in unkey:
                        self.data.append(max_obj)
                        unkey.append(full_path)

        # find by reg
        found_lst = []
        self.find_value("SOFTWARE\\Autodesk\\3dsMax\\", found_lst, flag=KEY_WOW64_64KEY)
        self.find_value("SOFTWARE\\Autodesk\\3dsMax\\", found_lst, flag=KEY_WOW64_32KEY)
        for root in found_lst:
            full_path = os.path.join(root, '3dsmax.exe')
            if os.path.exists(full_path):

                bit = self.get_app_bit(full_path)
                version = self.get_app_version(full_path)
                version_str = str(2000 + (int(version.split('.')[0]) - 2))
                if int(version.split('.')[0]) < 10:
                    version_str = str(('.'.join(version.split('.')[:2])))
                icon = self.get_app_icon(root, full_path, icon_found_path)

                user_path = os.environ["LOCALAPPDATA"]
                max_local_folder = os.path.join(user_path, 'Autodesk\\3dsMax', '{} - {}bit'.format(version_str, bit))

                max_data = {'path': full_path,
                            'local_path': max_local_folder,
                            'bit': bit,
                            'icon': icon,
                            'version': int(version.replace('.', '')),
                            'version_string': '3dsmax {}'.format(version_str)
                            }

                from cgtools.Autodesk3dsmax import Autodesk3dsmax
                max_obj = Autodesk3dsmax()
                max_obj.ready_data_from_finder(max_data)

                if full_path not in unkey:
                    self.data.append(max_obj)
                    unkey.append(full_path)

        self.data = sorted(self.data)


class PhotoShopFinder(FindBase):

    def __str__(self):
        return 'Adobe PhotoShop'

    def __getitem__(self, version, bit=64):
        return self.get_data_by_version(version, bit)

    def find_value(self, key_path, found_lst, spcae=winreg.HKEY_CURRENT_USER, *agrs):
        try:
            open_key = winreg.OpenKey(spcae, key_path, 0, KEY_ALL_ACCESS)
        except:
            return

        count_key = winreg.QueryInfoKey(open_key)[1]
        count_key = int(count_key)

        for i in range(count_key):
            name_tuple = winreg.EnumValue(open_key, i)
            name = name_tuple[0].lower()

            if 'photoshop.exe' in name.lower():
                path = name.split('photoshop.exe')[0]

                exe_filename = path + 'photoshop.exe'
                if exe_filename not in found_lst:
                    found_lst.append(exe_filename)

        return found_lst

    def find(self):
        found_lst = []

        # E:\PhotoShop\Adobe Photoshop CC 2015\Photoshop.exe.FriendlyAppName
        # HKEY_CURRENT_USER\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache"
        self.find_value(
            "Software\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\Shell\\MuiCache",
            found_lst,
            spcae=winreg.HKEY_CURRENT_USER
        )

        for full_path in found_lst:

            if os.path.exists(full_path):

                bit = self.get_app_bit(full_path)

                version = self.get_app_version(full_path)

                version_str = str(2000 + (int(version.split('.')[0]) - 1))

                if int(version.split('.')[0]) < 10:
                    version_str = str(('.'.join(version.split('.')[:2])))

                icon_found_path = (
                    '{}/AMT/Core key files/ProductIcon/ps.ico',
                )

                icon = self.get_app_icon(os.path.dirname(full_path), full_path, icon_found_path)

                ps_local_folder = ""

                ps_data = {
                    'path': full_path,
                    'local_path': ps_local_folder,
                    'bit': bit,
                    'icon': icon,
                    'version': int(version.replace('.', '')),
                    'version_string': 'Photoshop {}'.format(version_str)
                }

                from cgtools.AdobePhotoshop import AdobePhotoshop

                ps_obj = AdobePhotoshop()
                ps_obj.ready_data_from_finder(ps_data)

                self.data.append(ps_obj)
