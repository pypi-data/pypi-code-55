import os
import re
from diarypy.diary import Diary
from diarypy import DESCR_FILENAME
from diarypy import DIARY_VERSION_DELIMITER


def open_all_diaries(name, path, mode='r'):
    folder_regexp = re.compile(".*{0}{1}{2}\d+".format(os.path.sep, name,
                                                   DIARY_VERSION_DELIMITER))
    diary_dict = {}
    for root, subdirs, files in os.walk(path, followlinks=True):
        if folder_regexp.match(root) and (DESCR_FILENAME in files):
            try:
                diary_dict[root] = load_diary(root, mode=mode)
            except ValueError as e:
                print('Diary {} can not be loaded (skipped)'.format(root))
                print(e)
    return diary_dict

def load_diary(path, mode='r'):
    diary = Diary(name=None, path=path, overwrite=True, mode=mode)
    return diary
