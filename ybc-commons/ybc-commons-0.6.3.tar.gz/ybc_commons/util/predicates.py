import os
import re

from ybc_commons.oss import path
from ybc_exception import FilenameTooLongError
from ybc_exception import IllegalFilenameError
from . import Predicate


@Predicate
def true(*_):
    return True


@Predicate
def false(*_):
    return False


@Predicate
def is_truthy(value):
    return bool(value)


@Predicate
def is_falsy(value):
    return not value


@Predicate
def is_empty(value):
    return not value


@Predicate
def non_empty(value):
    return bool(value)


@Predicate
def non_blank(value):
    return bool(str.strip(str(value)))


@Predicate
def is_valid_filename(filename):
    # 合法 url 跳过检查
    if re.match(r'(http[s]?://([\w-]+\.)+(([\w\-/.?%&=])*))', filename):
        return True

    # _____temp 文件夹跳过路径检查
    # 传入路径时先判断文件夹是否存在，不存在抛出 FileNotFoundError，存在则 split 逐项检测是否合法
    if '_____temp' not in filename:
        path.url_of(os.path.dirname(filename), is_new_file=False)

    names = filename.split("/")
    for name in names:
        if not re.match(r'^[\u4e00-\u9fa5\w.\-()]+$', name):
            raise IllegalFilenameError("'" + filename + "'")

        # 文件名长度限制不包含后缀名
        name = os.path.splitext(name)[0]
        if not len(re.sub(r'[\u4e00-\u9fa5]', 'aa', name)) < 41:
            raise FilenameTooLongError(("'" + filename + "'"))
    return True


@Predicate
def is_function(value):
    return callable(value)


def match_regex_ignorecase(regex_str):
    @Predicate
    def inner(value):
        return bool(re.match(regex_str, value, re.IGNORECASE))

    return inner


def is_self(self):
    @Predicate
    def inner(value):
        return value is self

    return inner


def equals(other):
    @Predicate
    def inner(value):
        return value == other

    return inner


def is_instance_of(type):
    @Predicate
    def inner(value):
        return isinstance(value, type)

    return inner


def is_greater_than(lower):
    @Predicate
    def inner(value):
        return value > lower

    return inner


def is_greater_or_equal(lower):
    @Predicate
    def inner(value):
        return value >= lower

    return inner


def is_less_than(upper):
    @Predicate
    def inner(value):
        return value < upper

    return inner


def is_less_or_equal(upper):
    @Predicate
    def inner(value):
        return value <= upper

    return inner


def is_in(iterable):
    @Predicate
    def inner(value):
        return value in iterable

    return inner


def is_in_range(lower, upper):
    @Predicate
    def inner(value):
        return lower <= value < upper

    return inner


def has_len_in_range(lower, upper):
    @Predicate
    def inner(value):
        return lower <= len(value) < upper

    return inner


def file_format_in(*formats):
    @Predicate
    def inner(filename):
        return any(filename.lower().endswith('.' + format) for format in formats)

    return inner


@Predicate
def is_image_file(filename):
    image_file_extensions = ['.jpg', '.jpeg', '.png']
    return any(filename.lower().endswith(extension) for extension in image_file_extensions)


@Predicate
def is_audio_file(filename):
    audio_file_extensions = ['.mp3', '.wav', '.mp4']
    return any(filename.lower().endswith(extension) for extension in audio_file_extensions)
