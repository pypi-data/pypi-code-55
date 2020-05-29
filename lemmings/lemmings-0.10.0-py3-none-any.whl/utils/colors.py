import os
from lemmings.utils.utils import ignore_exception


def esc(code):
    enabled = os.getenv("ansi_colors", False) # by default, ansi colors are disabled
    return f"\033[{code}m" if enabled else ""

class Color:
    black, red, green, yellow, blue, magenta, cyan, white = 0, 1, 2, 3, 4, 5, 6, 7

    e = esc(0)  # End of color

    @classmethod
    def _(cls, typ, color, bright):
        b = ";1" if bright else ""
        return esc(f"{typ}{color}{b}")

    @classmethod
    def _foreground(cls, color, bright=False):
        return cls._(3, color, bright)

    @classmethod
    def _light(cls, color, bright=False):
        return cls._(9, color, bright)

    @classmethod
    def _background(cls, color, bright=False):
        return cls._(4, color, bright)

    @classmethod
    @ignore_exception
    def execute(cls, cmd, msg):
        return cmd + str(msg) + cls.e

    @classmethod
    def bold(cls, msg):
        return Color.execute(esc(1), msg)

    @classmethod
    def cursive(cls, msg):
        return Color.execute(esc(3), msg)

    @classmethod
    def underline(cls, msg):
        return Color.execute(esc(4), msg)

    @classmethod
    def mark(cls, color, msg):
        return Color.execute(Color._foreground(color), msg)

    @classmethod
    def back(cls, color, msg):
        return Color.execute(Color._background(color), msg)

    @classmethod
    @ignore_exception
    def print(cls, color, msg, comment="", prefix=""):
        back, fore = cls.list[color % len(cls.list)]
        s = prefix + back + fore + str(msg) + cls.e + str(comment)
        print(s)

Color.list = [
    (Color._background(Color.black), Color._light(Color.white)),
]
