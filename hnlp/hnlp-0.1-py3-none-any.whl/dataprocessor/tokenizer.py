from dataclasses import dataclass
import re

from torchtext.data import get_tokenizer


# referenced from jieba
re_zh = re.compile(r"([\u4E00-\u9FD5+#&\._%\-]+)", re.U)
re_skip = re.compile(r"(\s)", re.U)


class Tokenizer():
    pass


@dataclass
class BasicTokenizer:
    pass


@dataclass
class ChineseCharTokenizer(BasicTokenizer):

    def cut(self, text: str):
        blocks = re_zh.split(text)
        for block in blocks:
            if not block:
                continue
            if re_zh.match(block):
                for char in block:
                    yield char
            else:
                skips = re_skip.split(block)
                for skip in skips:
                    if skip:
                        yield skip

    def __call__(self, text: str):
        return list(self.cut(text))


@dataclass
class ChineseWordTokenizer(BasicTokenizer):
    segmentor: callable

    def cut(self, text: str):
        for token in segmentor(text):
            yield token

    def __call__(self, text: str):
        return list(self.cut(text))
