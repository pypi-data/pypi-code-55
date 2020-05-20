from typing import Dict, Union, Callable

from matplotlib.text import Text

from mpl_format.text.text_utils import wrap_text, remove_parenthesized_text


class TextFormatter(object):

    def __init__(self, text: Text):
        """
        Create a new TextFormatter for a matplotlib Text instance.

        :param text: The matplotlib Text instance to wrap.
        """
        self._text: Text = text

    @property
    def text(self) -> Text:
        """
        Return the wrapped matplotlib Text instance.
        """
        return self._text

    def to_string(self) -> str:
        """
        Return the text of the wrapped matplotlib Text instance.
        """
        return self._text.get_text()

    def wrap(self, max_width: int) -> 'TextFormatter':
        """
        Wrap the text with new lines if it exceeds a given width of characters.

        :param max_width: The maximum character width per line.
        """
        wrapped = wrap_text(self.to_string(), max_width=max_width)
        self._text.set_text(wrapped)
        return self

    def rotate(self, rotation: Union[str, int], how: str = 'absolute') -> 'TextFormatter':
        """
        Set the rotation of the text.

        :param rotation: The rotation value to set in degrees, 'horizontal' or 'vertical'.
        :param how: 'absolute' or 'relative'
        """
        if how == 'relative' and not isinstance(rotation, str):
            self._text.set_rotation(self._text.get_rotation() + rotation)
        elif how == 'absolute':
            self._text.set_rotation(rotation)
        else:
            raise ValueError("`how` must be 'absolute' or 'relative'")
        return self

    def map(self, mapping: Union[Dict[str, str], Callable[[str], str]]) -> 'TextFormatter':
        """
        Replace label text if it matches one of the dictionary keys.

        :param mapping: Mappings to replace text.
        """
        if isinstance(mapping, dict):
            if self.to_string() in mapping.keys():
                self._text.set_text(mapping[self.to_string()])
        elif callable(mapping):
            self._text.set_text(mapping(self.to_string()))
        else:
            raise TypeError('mapping must be a dict or callable')
        return self

    def remove_parenthesized_text(self) -> 'TextFormatter':
        """
        Remove any text inside parentheses, along with the parentheses.
        """
        self._text.set_text(remove_parenthesized_text(self.to_string()))
        return self

    def replace(self, old: str, new: str) -> 'TextFormatter':
        """
        Replace old text with new text.

        :param old: The text to remove.
        :param new: The text to insert.
        """
        self._text.set_text(
            self.to_string().replace(old, new)
        )
        return self

    def set_text(self, text: str) -> 'TextFormatter':
        """
        Set the text string.
        """
        self._text.set_text(text)

    def set_size(self, font_size) -> 'TextFormatter':
        """
        Set the font size for the Text.
        """
        self._text.set_fontsize(font_size)
        return self
    
    def set_size_xx_small(self):
        self.set_size('xx-small')
        return self

    def set_size_x_small(self):
        self.set_size('x-small')
        return self

    def set_size_small(self):
        self.set_size('small')
        return self

    def set_size_medium(self):
        self.set_size('medium')
        return self

    def set_size_large(self):
        self.set_size('large')
        return self

    def set_size_x_large(self):
        self.set_size('x-large')
        return self

    def set_size_xx_large(self):
        self.set_size('xx-large')
        return self

    def set_size_larger(self):
        self.set_size('larger')
        return self

    def set_size_smaller(self):
        self.set_size('smaller')
        return self

    def clear(self) -> 'TextFormatter':
        """
        Clear the text string.
        """
        self.set_text('')
        return self
