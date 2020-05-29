import os
import sys
import requests

from ybc_config import config

if sys.platform == 'win32':
    HOME_DRIVE_KEY = 'HOMEDRIVE'
    HOME_PATH_KEY = 'HOMEPATH'
    _DEFAULT_USER_WORKSPACE_ROOT = (
        r'{}{}\AppData\Roaming\Prometheus\Application Data\workspace'
        .format(os.environ[HOME_DRIVE_KEY], os.environ[HOME_PATH_KEY])
    )
else:
    _DEFAULT_USER_WORKSPACE_ROOT = '/sandbox'
_USER_WORKSPACE_ROOT = os.environ.get('USER_WORKSPACE_ROOT', _DEFAULT_USER_WORKSPACE_ROOT)
_OSS_ENDPOINT = config['prefix-oss']
_PUBLIC_FILES_UPLOAD_API = config['course-api-prefix'] + "/public-files"


def url_of(filename, is_new_file=False):
    """
    获取文件在 OSS 上的 URL

    :param filename: 文件相对于当前工作目录的路径, 比如 '1.jpg', '../1.jpg', './1.jpg' 等
    :param is_new_file: 是否是待创建的新文件, 如果是待创建的新文件, 则不需要检查文件是否存在
    :return: 文件在 OSS 上的 URL
    """
    if not filename or (filename.startswith('https://')
                        or filename.startswith('http://')):
        return filename
    elif os.path.isdir(filename):
        # 不对文件夹进行转换，只判断是不是存在的文件夹
        return filename
    elif is_new_file:
        # 获取文件在文件系统中的绝对路径
        local_file_path = os.path.abspath(filename)
        # 获取文件相对于用户根目录的相对路径
        # 比如: 41314233/default/turtle/wc/1.jpg
        oss_file_path = os.path.relpath(local_file_path, _USER_WORKSPACE_ROOT).replace('\\', '/')
        # 拼接出文件在 OSS 上的 URL
        return '{}/{}'.format(_OSS_ENDPOINT, oss_file_path)
    else:
        with open(filename, 'rb') as f:
            # 上传文件，生成 URL
            response = requests.post(_PUBLIC_FILES_UPLOAD_API, files={'file': f})
            if response.ok:
                public_file = response.json()
                return public_file['url']
            else:
                raise RuntimeError()
