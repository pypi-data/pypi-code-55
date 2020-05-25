"""API for console manipulation using ANSI Escape sequences in Python.
"""
import logging
from itertools import chain
from pyansiescapes.enums import ANSICommands, TextAttributes, ColorDrawingLevel, Colors
from pyansiescapes import utils
import pyansiescapes._types as t

_logger = logging.getLogger(__file__)


# Curser controls:
def cursor_up(number_of_lines: int = 1) -> str:
    """Moves cursor up number_of_lines lines."""
    return ANSICommands.start + "{:d}A".format(number_of_lines)


def cursor_down(number_of_lines: int = 1) -> str:
    """Moves cursor down number_of_lines lines."""
    return ANSICommands.start + "{:d}B".format(number_of_lines)


# Clearers:
def clear_to_end_of_line() -> str:
    """Clears line from current cursor position to the end."""
    return ANSICommands.start + "0K"


def clear_to_start_of_line() -> str:
    """Clears line from start to current cursor position."""
    return ANSICommands.start + "1K"


def clear_line() -> str:
    """Clears the entire line from start to end."""
    return ANSICommands.start + "2K"


def clear_lines(number_of_lines: int = 1) -> str:
    """Clears number_of_lines lines."""
    return (clear_line() + cursor_up()) * number_of_lines


def clear_screen_until_end() -> str:
    """Clears screen from current cursor position to the end."""
    return ANSICommands.start + "0J"


def clear_screen_to_beginning() -> str:
    """Clears screen from current cursor position to the beginning."""
    return ANSICommands.start + "1J"


def clear_screen() -> str:
    """Clears the entire screen. """
    return ANSICommands.start + "2J"


# Rich Text formatting:

def format(text: str, *args: t.Any, **kwargs: t.Any) -> str: # pylint: disable=redefined-builtin
    """Return formatted text as str.

    Uses the formatting attributes given in `*args` or `**kwargs`.
    Postional arguments or keywordarguments that are not supported
    will be ignored.

    Args:
        text: The text/string that should be formatted.
        *args: Any number of postional arguments. Unsupported arguments will be
            ignored. See "supported arguments" section for futher details.
        **kwargs: Any number of keyword arguments. Unsupported keyword arguments
            will be ignored. See "supported keywords" section for further
            details.

    Returns:
        The text with leading ANSI Escape sequence "rich text"
        commands and a trailing ANSI Escape sequence "reset"
        command.

    Examples:
        >>> # Format text to bold and underlined using postional arguments
        >>> format('Hello ANSI!', 'bold', 'underline')
        \'\\x1b[1;4mHello ANSI!\\x1b[0m\'

        >>> # It's also possible to use keyword arguments with True, False
        >>> format('Hello ANSI!', bold=True, underline=True)
        \'\\x1b[1;4mHello ANSI!\\x1b[0m\'

        >>> # You can also set font and background color
        >>> format('Hello ANSI!', color='blue', background='white')
        \'\\x1b[34;47mHello ANSI!\\x1b[0m\'

        >>> # Or provide a keyword argument dict
        >>> format('Hello ANSI!', color={'name':'blue', 'colormode':256}, background='white')
        \'\\x1b[38;5;12;47mHello ANSI!\\x1b[0m\'
    """
    # parse positional text attributes
    text_attribute_arguments = (arg for arg in args
                                if arg in TextAttributes.__members__.keys()) # pylint: disable=no-member
    # parse keyword text attribute arguments:
    text_attribute_keywords = (
        kwarg for kwarg, value in kwargs.items()
        if value and kwarg in TextAttributes.__members__.keys()) # pylint: disable=no-member
    text_attributes = (
        TextAttributes[key]
        for key in chain(text_attribute_arguments, text_attribute_keywords))
    # parse positional
    color_attributes = []
    for i, key in enumerate(["color", "background"]):
        try:
            value = kwargs[key]
        except KeyError:
            continue
        if isinstance(value, (tuple, list)):
            attribute = _color(*value, drawing_level=i)
        elif isinstance(value, dict):
            attribute = _color(**value, drawing_level=i)
        else:
            attribute = _color(value, drawing_level=i)

        color_attributes.append(attribute)

    return _format_rich_text(*text_attributes, *
                             color_attributes) + text + reset()


# TextAttributes:
def reset() -> str:
    """Returns 'reset' ANSI-command string."""
    return _format_rich_text(TextAttributes.reset)


def bold() -> str:
    """Returns 'bold text' ANSI-command string."""
    return _format_rich_text(TextAttributes.bold)


def underscore() -> str:
    """Returns 'underlined/underscored text' ANSI-command string."""
    return _format_rich_text(TextAttributes.underscore)


def underline() -> str:
    """Returns 'underlined/underscored text' ANSI-command string."""
    return _format_rich_text(TextAttributes.underline)


def bright() -> str:
    """Returns 'bright/blink text' ANSI-command string."""
    return _format_rich_text(TextAttributes.bright)


def blink() -> str:
    """Returns 'bright/blink text' ANSI-command string."""
    return _format_rich_text(TextAttributes.blink)


def reversed() -> str: # pylint: disable=redefined-builtin
    """Returns 'reversed text' ANSI-command string."""
    return _format_rich_text(TextAttributes.reversed)


def concealed() -> str:
    """Returns 'concealed text' ANSI-command string."""
    return _format_rich_text(TextAttributes.concealed)


# Colors:
def color(*args: t.Any, **kwargs: t.Any) -> str:
    """Returns ANSI Escape Sequence for specified color.

    Args:
        *args: any valid positional argument for :func:`._color`.
        **kwargs: any valid keyword argument for :func:`._color`.

    Examples:
        >>> # Get string for 8-bit red text coloring (e.g. foreground).
        >>> color(name="red")
        \'\\x1b[31m\'

        >>> # Get string for bold red background.
        >>> color(name="red", bold=True, drawing_level="background")
        \'\\x1b[41;1m\'

        >>> # Get string for 256-bit red background.
        >>> color(name="red", bold=True, blink=True, drawing_level="background")
        \'\\x1b[48;5;9m\'

        >>> # Get string for mediumspringgreen foreground 256-bit color.
        >>> color(name="mediumspringgreen")
        \'\\x1b[38;5;49m\'

    """
    return _format_rich_text(_color(*args, **kwargs))


def _color(name: t.Optional[t.ColorArg] = None, # pylint: disable=too-many-arguments
           color_id: t.Optional[t.Union[int, str]] = None,
           hexa: t.Optional[str] = None,
           rgb: t.Optional[t.ColorValue] = None,
           hsl: t.Optional[t.ColorValue] = None,
           drawing_level: t.DrawingLevelArg = ColorDrawingLevel.foreground,
           bold: bool = False, # pylint: disable=redefined-outer-name
           blink: bool = False, # pylint: disable=redefined-outer-name
           bright: bool = False, # pylint: disable=redefined-outer-name
           colormode: int = 8) -> str:
    """Returns ANSI color-string for specified color.

    Color value argument get parsed in this order:

    - \(0) colorid, (1) name, (2) hexa, (3) rgb, (4) hsl.

    Colormode gets toggled in this order:

    - Conditions for 256-bit colormode are checked first:
        - :py:`color_id is not None and color_id > 8`
        - :py:`name not in` :class:`.Colors` or ``name`` is in hexa-, rgb- or
          hsl-format (see below)
        - :py:`any(hexa, rgb, hsl)`
        - :py:`bright or blink or colormode == 256`

    - Next the condition for 16-bit colormode are checked:
        - :py:`((color_id < 8 or name in` :class:`.Colors` :py:`) and bold)`
          :py:`or colormode == 16`

    - If none of the above conditions are true, fallback to default
        8-bit colormode.

    Args:
        name: A color name.
            Can be of format:

            - Any name in :class:`.Colors` or :class:`.Colors256`.
            - Integer or Integer-string (triggers color id parsing.)
                - Strings with leading ``#`` (triggers hex-value parsing.)
            - Tuple, list or array-like (triggers parsing as either rgb- or
              hsl-values based on the input values.)

            See :func:`.utils.parse_color_name` for details on parsing logic.
        color_id: The color id as integer or integer-string.
        hexa: A hexadecimal color value as str. Must start with a leading ``#``.

            See :func:`.utils.parse_hex` for details on parsing logic.
        rgb: Color values in rgb color space. Must be iterable and of length 3.
            See :func:`.utils.parse_color_value` for details on parsing logic.
        hsl: Color values in hsl color space. Must be iterable and of lenght 3.
            See :func:`.utils.parse_color_value` for detail on parsing logic.
        drawing_level:
            The color drawing level.

            Valid foreground values are:
                - :py:`'foreground'`, :attr:`.ColorDrawingLevel.foreground`,
                  :py:`0`, :py:`False`, :py:`'3'`

            Valid background values are:
                - ``'background'``, :attr:`.ColorDrawingLevel.background`,
                  :py:`1`, :py:`True`, :py:`'4'`

            Default: :py:`"foreground"`
        bold: Triggers bold colors (16-bit).
            Default: False
        blink: Triggers "blink/birght" colors (256-bit).
            Deafault: False
        bright: Triggers "blink/birght" colors (256-bit).
            Default: False
        colormode: Triggers 8-, 16-, or 256-bit colors. Any in (8, 16, 256).
            Default: 8

    Raises:
        TypeError: If all color arguments are None.
    """
    # Parse drawing level
    drawing_level = utils.parse_drawing_level(drawing_level)
    colormode = utils.parse_colormode(colormode, blink, bright, bold)
    _logger.debug("%d", colormode)
    # Check if a valid color was provided
    argc, arg = utils.get_first_color_argument(color_id, name, hexa, rgb, hsl)
    # Look-up correct get color id function
    get_color_id = utils.parsing_switcher(argc, arg)
    color_id, colormode = get_color_id(arg, colormode)
    _logger.debug("%s, %d", color_id, colormode)
    color_string = utils.get_color_string(color_id, colormode)

    return drawing_level + color_string


# convenience functions:
def color_8bit(
        name: str,
        drawing_level: t.DrawingLevelArg = ColorDrawingLevel.foreground
) -> str:
    """Convenience function for 8-bit colors.

    Trys to find the color_id for provided name. Returns an empty string if name
    is not an 8-bit color.

    Args:
        name: A color name. Any color name in Colors.
        drawing_level: The color drawing level.

            Valid foreground values are:
                - "foreground", :attr:`.ColorDrawingLevel.foreground`, 0, "3"

            Valid background values are:
                - "background", :attr:`.ColorDrawingLevel.background`, 1, "4"

            Default: "foreground"

    """
    if utils.is_8bit_color(name):
        drawing_level = utils.parse_drawing_level(drawing_level)
        return _format_rich_text(drawing_level + Colors[name])
    return ""


def background(*args: t.Any, **kwargs: t.Any) -> str:
    """Convenience function for colored backgrounds.

    Returns a call to :func:`.color` with drawing_level= :attr:`.ColorDrawingLevel.background`.
    See color for further description of input arguments. Drawing_level keyword
    argument should be omitted."""
    return color(*args, **kwargs, drawing_level=ColorDrawingLevel.background)


def black(
        drawing_level: t.DrawingLevelArg = ColorDrawingLevel.foreground
) -> str:
    """Convenience function for 8-bit black color.

	See :func:`.color_8bit` for further details.
	"""
    return color_8bit("black", drawing_level)


def red(drawing_level: t.DrawingLevelArg = ColorDrawingLevel.foreground
        ) -> str:
    """Convenience function for 8-bit red color.

	See :func:`.color_8bit` for further details.
	"""
    return color_8bit("red", drawing_level)


def green(
        drawing_level: t.DrawingLevelArg = ColorDrawingLevel.foreground
) -> str:
    """Convenience function for 8-bit green color.

	See :func:`.color_8bit` for further details.
	"""
    return color_8bit("green", drawing_level)


def yellow(
        drawing_level: t.DrawingLevelArg = ColorDrawingLevel.foreground
) -> str:
    """Convenience function for 8-bit yellow color.

	See :func:`.color_8bit` for further details.
	"""
    return color_8bit("yellow", drawing_level)


def blue(
        drawing_level: t.DrawingLevelArg = ColorDrawingLevel.foreground
) -> str:
    """Convenience function for 8-bit blue color.

	See :func:`.color_8bit` for further details.
	"""
    return color_8bit("blue", drawing_level)


def magenta(
        drawing_level: t.DrawingLevelArg = ColorDrawingLevel.foreground
) -> str:
    """Convenience function for 8-bit magenta color.

	See :func:`.color_8bit` for further details.
	"""
    return color_8bit("magenta", drawing_level)


def cyan(
        drawing_level: t.DrawingLevelArg = ColorDrawingLevel.foreground
) -> str:
    """Convenience function for 8-bit cyan color.

	See :func:`.color_8bit` for further details.
	"""
    return color_8bit("cyan", drawing_level)


def white(
        drawing_level: t.DrawingLevelArg = ColorDrawingLevel.foreground
) -> str:
    """Convenience function for 8-bit white color.

	See :func:`.color_8bit` for further details.
	"""
    return color_8bit("white", drawing_level)


def _format_rich_text(*formatting_commands: str) -> str:
    """Return an ANSI Escapes Sequence for rich text formatting.

    Mutiple formatting commands are chained using the ANSI command seperator.
    """
    ansi_command = ANSICommands.start
    logging.debug("_format_rich_text received: %s",
                  (", ".join(formatting_commands)))
    ansi_command += ANSICommands.separator.join(formatting_commands)
    ansi_command += ANSICommands.stop
    logging.debug("%s", ANSICommands._debug_esc + ansi_command[1:]) # pylint: disable=protected-access
    return ansi_command


if __name__ == '__main__':
    import doctest
    doctest.testmod()
