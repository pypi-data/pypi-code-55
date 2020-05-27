# coding=utf-8
import re
import unidecode


class PatternNormalizer(object):
    AC_REGEX = r"\/([acAC]+)(\s)?$"

    def __init__(self):
        self.normalizers = {
            "a": self.fold_ascii,
            "c": self.fold_case
        }

    def parse(self, string):
        """
        :param string:
        :return:
        """
        r = re.compile(self.AC_REGEX, re.IGNORECASE)
        s = r.search(string)
        removed_ac = r.sub("", string)
        if s:
            return removed_ac, list(s.groups()[0])
        return removed_ac, []

    def remove_ac(self, string):
        r = re.compile(self.AC_REGEX, re.IGNORECASE)
        return r.sub("", string)

    @staticmethod
    def fold_case(string):
        return string.replace(u'I', u'ı').replace(u'İ', u'i').lower()

    @staticmethod
    def fold_ascii(string):
        return unidecode.unidecode(string)

    @staticmethod
    def strip_whitespace(string):
        return ' '.join(string.split())

    def normalize(self, pattern, strip_whitespace=True, _normalizers=None):
        """
        :param pattern: string
        :param strip_whitespace:
        :param _normalizers: list ["a"], ["c"], ["a", "c"]
        :return:
        """
        raw, normalizers = self.parse(pattern)
        if _normalizers:
            normalizers = _normalizers
        for op in normalizers:
            raw = self.normalizers[op.lower()](raw)
        if strip_whitespace:
            raw = self.strip_whitespace(raw)
        return raw