import subprocess
import os
import platform


def xopen():
    pre_path = os.path.expanduser("~/学而思直播/code/cache/")

    project_path = os.getcwd()
    if platform.system() == "Windows":
        os.startfile(project_path )
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", project_path ])
    else:
        subprocess.Popen(["xdg-open", project_path ])