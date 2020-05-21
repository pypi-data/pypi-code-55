#!/usr/bin/python3
from printj.lib import Template
import os


class say:
    def __init__(self, text):
        os.system(f'spd-say "  {text} "')


class bold:
    # color = 'red'

    def __init__(self, text):
        print(Template.stylish_text(text=text, style='bold'))


class italic:
    # color = 'red'

    def __init__(self, text):
        print(Template.stylish_text(text=text, style='italic'))


class ColorPrint:
    color = 'red'

    def __init__(self, text):
        self.text = text

    # On a background
    @classmethod
    def on_black(cls, text):
        print(Template.highlight_text(text=text, front=cls.color, back='black'))

    @classmethod
    def on_red(cls, text):
        print(Template.highlight_text(text=text, front=cls.color, back='red'))

    @classmethod
    def on_green(cls, text):
        print(Template.highlight_text(text=text, front=cls.color, back='green'))

    @classmethod
    def on_yellow(cls, text):
        print(Template.highlight_text(text=text, front=cls.color, back='yellow'))

    @classmethod
    def on_blue(cls, text):
        print(Template.highlight_text(text=text, front=cls.color, back='blue'))

    @classmethod
    def on_purple(cls, text):
        print(Template.highlight_text(text=text, front=cls.color, back='purple'))

    @classmethod
    def on_cyan(cls, text):
        print(Template.highlight_text(text=text, front=cls.color, back='cyan'))

    @classmethod
    def on_white(cls, text):
        print(Template.highlight_text(text=text, front=cls.color, back='white'))

    # Bold on a background
    @classmethod
    def bold_on_black(cls, text):
        print(Template.highlight_text(text=text, style='bold', front=cls.color, back='black'))

    @classmethod
    def bold_on_red(cls, text):
        print(Template.highlight_text(text=text, style='bold', front=cls.color, back='red'))

    @classmethod
    def bold_on_green(cls, text):
        print(Template.highlight_text(text=text, style='bold', front=cls.color, back='green'))

    @classmethod
    def bold_on_yellow(cls, text):
        print(Template.highlight_text(text=text, style='bold', front=cls.color, back='yellow'))

    @classmethod
    def bold_on_blue(cls, text):
        print(Template.highlight_text(text=text, style='bold', front=cls.color, back='blue'))

    @classmethod
    def bold_on_purple(cls, text):
        print(Template.highlight_text(text=text, style='bold', front=cls.color, back='purple'))

    @classmethod
    def bold_on_cyan(cls, text):
        print(Template.highlight_text(text=text, style='bold', front=cls.color, back='cyan'))

    @classmethod
    def bold_on_white(cls, text):
        print(Template.highlight_text(text=text, style='bold', front=cls.color, back='white'))

    # Italic on a background
    @classmethod
    def italic_on_black(cls, text):
        print(Template.highlight_text(text=text, style='italic', front=cls.color, back='black'))

    @classmethod
    def italic_on_red(cls, text):
        print(Template.highlight_text(text=text, style='italic', front=cls.color, back='red'))

    @classmethod
    def italic_on_green(cls, text):
        print(Template.highlight_text(text=text, style='italic', front=cls.color, back='green'))

    @classmethod
    def italic_on_yellow(cls, text):
        print(Template.highlight_text(text=text, style='italic', front=cls.color, back='yellow'))

    @classmethod
    def italic_on_blue(cls, text):
        print(Template.highlight_text(text=text, style='italic', front=cls.color, back='blue'))

    @classmethod
    def italic_on_purple(cls, text):
        print(Template.highlight_text(text=text, style='italic', front=cls.color, back='purple'))

    @classmethod
    def italic_on_cyan(cls, text):
        print(Template.highlight_text(text=text, style='italic', front=cls.color, back='cyan'))

    @classmethod
    def italic_on_white(cls, text):
        print(Template.highlight_text(text=text, style='italic', front=cls.color, back='white'))


class black(ColorPrint):
    color = 'black'

    def __init__(self, text):
        print(Template.color_text(text=text, front=black.color))
        super().__init__(text)


class red(ColorPrint):
    color = 'red'

    def __init__(self, text):
        print(Template.color_text(text=text, front=red.color))
        super().__init__(text)


class green(ColorPrint):
    color = 'green'

    def __init__(self, text):
        print(Template.color_text(text=text, front=green.color))
        super().__init__(text)


class yellow(ColorPrint):
    color = 'yellow'

    def __init__(self, text):
        print(Template.color_text(text=text, front=yellow.color))
        super().__init__(text)


class blue(ColorPrint):
    color = 'blue'

    def __init__(self, text):
        print(Template.color_text(text=text, front=blue.color))
        # super().__init__(text)


class purple(ColorPrint):
    color = 'purple'

    def __init__(self, text):
        print(Template.color_text(text=text, front=purple.color))
        super().__init__(text)


class cyan(ColorPrint):
    color = 'cyan'

    def __init__(self, text):
        print(Template.color_text(text=text, front=cyan.color))
        super().__init__(text)


class white(ColorPrint):
    color = 'white'

    def __init__(self, text):
        print(Template.color_text(text=text, front=white.color))
        super().__init__(text)


if __name__ == "__main__":
    red('Error, does not compute!')
    blue('Error, does not compute!')
    white('Error, does not compute!')
    # say('Error, does not compute!')
    red.on_green('Error, does not compute!')
    white.bold_on_green('Error, does not compute!')
    blue.on_green('Error, does not compute!')
    red(Template.stylish_text(text='Error, does not compute!', style='bold'))
