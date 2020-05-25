"""Utility functions used by pyansiescapes.

Provides functions for either parsing arguments, getting correct ids from
ANSI-Enums, or checking for correct types, format etc.

"""

from pyansiescapes.enums import ANSICommands, TextAttributes, ColorDrawingLevel, Colors, Colors256
import pyansiescapes._types as t
from collections.abc import Iterable
import logging

_logger = logging.getLogger(__file__)
#--------------------- Parsers ------------------------------
def parsing_switcher(argc: int, arg: t.ColorArg) -> t.Callable[[t.ColorArg, int], t.Tuple[str, int]]:
    """Return get color_id function for argument arg.

    If argument is 'name', parse name first to check if user did not
    provide a hexadecimal, rgb or hsl value.

    Args:
        argc: The positional argument count [1-4] which specifies the argument type.

        arg: The color argument.

    Returns:
        The get_color_id_from_{type} function obj.
        Any of :func:`.get_color_id_from_id`, :func:`.get_color_id_from_name`,
        :func:`.get_color_id_from_hex` or
        :func:`.get_color_id_from_color_value`
    """
    switcher = {
        0: get_color_id_from_id,
        1: get_color_id_from_name,
        2: get_color_id_from_hex,
        3: lambda x, y: get_color_id_from_color_value(x, y, "rgb"),
        4: lambda x, y: get_color_id_from_color_value(x, y, "hsl"),
    }
    if argc == 1:
        # parse color name and then check again
        argc, arg = parse_color_name(arg)

    return switcher[argc]


def parse_drawing_level(drawing_level: t.DrawingLevelArg) -> str:
    """Parse drawing level into legal ANSI drawing level Sequence."""
    if isinstance(drawing_level, int):
        try:
            drawing_level = list(ColorDrawingLevel)[drawing_level]
        except IndexError:
            raise KeyError(
                "Cannot parse {} into type ColorDrawingLevel".format(drawing_level))

    elif not isinstance(drawing_level, ColorDrawingLevel):
        if drawing_level in ["3", "4"]:
            drawing_level = drawing_level
        else:
            try:
                drawing_level = ColorDrawingLevel[drawing_level]
            except KeyError:
                raise KeyError(
                    "Cannot parse {} into type ColorDrawingLevel".format(drawing_level))

    return drawing_level


def parse_colormode(colormode: int, blink: bool,
                    bright: bool, bold: bool) -> int:
    """Parse colormode setters into colormode.

    Returns the colormode in int. Blink and Bright will override colormode.
    Bold overrides colormode if :py:`colormode == 8`.

    Args:
        colormode: Colormode for colors. Any in :py:`[8, 16, 256]`.
        blink: Toggle blink/bright/256 bit mode.
        bright: Toggle blink/bright/256 bit mode.
        bold: Toggle bold/16-bit mode.

    Returns:
        Either 8, 16 or 256 (as integer) corresponding to the colormode.
    """
    if blink or bright or colormode == 256:
        colormode = 256
        return colormode
    elif bold or colormode == 16:
        colormode = 16
        return colormode
    else:
        return colormode


def parse_color_name(name: t.ColorArg) -> t.ColorArgTuple:
    """Parses the color name.

    Args:
        name: A color name. Can be any name in :class:`.Colors` or :class:`.Colors256` as :py:`str`.
            Strings with leading ``#`` will trigger hex value parsing.
            Tuple, list or array-like will trigger parsing as either rgb-
            or hsl-values based on the input values.
            See :func:`._parse_rgb_or_hsl` for details on parsing logic.

    Returns:
        A tuple where the first value defines the color argument category and
        the second value is the color argument parse into the correct type.

    Examples:
        >>> # Color name string as name argument
        >>> parse_color_name(name="blue")
        (1, 'blue')

        >>> # Hexadecimal color value as "name" argument
        >>> parse_color_name(name="#ffffff")
        (2, '#ffffff')

        >>> # Rgb-values as "name" argument
        >>> parse_color_name((255, 0, 0))
        (3, (255, 0, 0))

        >>> # Color-id as "name" argument
        >>> parse_color_name(name=1)
        (0, 1)

        >>> # Color-id string as "name" argument
        >>> parse_color_name(name="1")
        (0, 1)

        >>> # Received incorrect argument for "name". Raise TypeError.
        >>> parse_color_name(name=None)
        Traceback (most recent call last):
        ...
        TypeError: Cannot understand \"name=None\" input argument type

    """
    try:
        name = int(name)
    except (ValueError, TypeError):
        pass
    # if name is and integer, its a color_id
    if isinstance(name, int):
        return 0, name
    elif not isinstance(name, str):
        # user provided rgb or hsl value
        if isinstance(name, Iterable):
            return 3, name
        else:
            # cannot understand input argument type
            raise TypeError(
                "Cannot understand \"name={}\" input argument type".format(name))
    elif name.startswith('#'):
        # user input name is a hex colorvalue
        return 2, name

    return 1, name


def parse_hex(hex: str) -> str:
    """Checks if hex is valid and return it in Colors256-key format.

    Args:
        hex: Hexadecimal color value. Must start with ``#``, be of length 7 and
            must be a valid hexadecimal value (all characters must be in
            :py:`set("#abcdef0123456789")`).

    Returns:
        The hexadecimal color value in Colors256-key-format (eg.
        :py:`"hex_ffffff"`).

    Raises:
        TypeError: {hex} is not a valid hexadecimal color value
            Raised if the input hex string is not valid.

    Examples:
        >>> # Parse white hexadecimal color value into Colors256-key.
        >>> parse_hex("#ffffff")
        'hex_ffffff'

        >>> # Raise TypeError with hexadecimal color value is wrong.
        >>> parse_hex("ffffff")
        Traceback (most recent call last):
        ...
        TypeError: \"ffffff\" is not a valid hexadecimal color value

        >>> # Raise TypeError with hexadecimal color value is wrong.
        >>> parse_hex("#gfffff")
        Traceback (most recent call last):
        ...
        TypeError: \"#gfffff\" is not a valid hexadecimal color value

    """
    if is_valid_hex_string(hex):
        hex = 'hex_' + hex[1:]
    else:
        raise TypeError(
            "\"{}\" is not a valid hexadecimal color value".format(hex))

    return hex


def parse_color_value(color_value: t.ColorValue, key: str) -> str:
    """Parses color value to color key

    RGB-values will be cliped to their respective closest bin.
    """
    if key == "rgb":
        color_value = clip_to_closes_color(color)
    return key + '_'.join((str(val) for val in rgb))


def parse_arguments(*args: t.Any) -> t.Iterator[t.ColorArgTuple]:
    """Yields arguments that are not None."""
    for argc, arg in enumerate(args):
        if arg is not None:
            yield (argc, arg)


def clip_to_closes_color(color: t.ColorValue) -> t.Iterator[int]:
    """Clips the rgb values to their respective closest bin."""
    assert isinstance(color, Iterable)

    bins = [0, 95, 135, 175, 215, 255]
    color = (_round_to_next_bin(x, bins) for x in color)
    return color


def _round_to_next_bin(val: int, bins: t.ColorBins) -> int:
    """Return the bin in bins closest to value."""
    right = bisect_right(bins, val)
    left = right - 1
    ret = _get_closest(val, *bins[left:right+ 1]
                       ) if right != len(bins) else bins[left]
    return ret


# ---------------------- Getters ---------------------------------------
def _get_closest(val: int, left: int, right: int) -> int:
    """Return left or right depending on which is closer to val"""
    ret = left if val - left < right - val else right
    return ret


def get_first_color_argument(*args: t.Any) -> t.ColorArgTuple:
    """Return first argument in args which is not None.

    Raises:
        TypeError: Cannot parse ``None`` into a color. Please provide a color!
            If all arguments are ``None``.
    """
    try:
        argc, arg = next(parse_arguments(*args))
    except StopIteration:
        raise TypeError(
            "Cannot parse 'None' into a color. Please provide a color!")

    return argc, arg


def get_color_id_from_id(color_id: int, colormode: int) -> t.Tuple[str, int]:
    """Return color_id as str and toggle colormode 256 if necessary."""
    if color_id > 8:
        colormode = 256
    return str(color_id), colormode


def get_color_id_from_color_enum(key: str, color_enum: t.ColorEnum) -> str:
    """Return color_id as str for key in color_enum

    Args:
        key: A Color key as str.
            Any of format:

                - name: :py:`"^[a-z, A-z, 0-9]*"` (e.g. :py:`"blue"`)
                - hex: :py:`"^hex_[0-9,a-f]{6}$"` (e.g. :py:`"hex_ffffff"`)
                - rgb: :py:`"^rgb_[0-9]{1,3}_[0-9]{1,3}_[0-9]{1,3}$"`
                  (e.g. :py:`"rbg_255_0_0"`)
                - hsl: :py:`"^hsl_[0-9]{1,3}_[0-9]{1,3}_[0-9]{1,3}$"`
                  (e.g. :py:`"hsl_255_0_0"`)

        color_enum: An enum-obj of type :class:`.Colors` or :class:`.Colors256`.

    Returns:
        A color id as str (:py:`"^[0-9]{1,3}$"` e.g. :py:`"102"`).

    Raises:
        KeyError: {key} is not a valid color key!
            If key is not a valid color key for Color Enum.
    """
    try:
        color_id = color_enum[key]
    except KeyError:
        raise KeyError("{} is not a valid color key for {}!".format(key, color_enum))
    return color_id


def get_color_id_from_name(name: str, colormode: int) -> t.Tuple[str, int]:
    """Returns a color id and the correct colormode.

    Parses name into all lower cases letters and toggles colormode 256 if
    name is not an 8-bit Color name.

    Args:
        name: A color name.
            Format:

                - :py:`'^[a-z, A-z, 0-9]*'` (e.g. :py:`"blue"`).

        colormode: Any integer in :py:`[8, 16, 256]`.
    """
    if colormode == 256:
        color_enum = Colors256
    else: # colormode != 256
        if not is_8bit_color(name):
            colormode = 256
            color_enum = Colors256
        else:
            color_enum = Colors

    return get_color_id_from_color_enum(name.lower(), color_enum), colormode


def get_color_id_from_hex(hex: str, colormode: int) -> t.Tuple[str, int]:
    """Returns a color id and the correct colormode.

    Parses hex str (e.g. :py:`"#ffffff"`) into valid key format (e.g. :py:`"hex_ffffff"`).

    Args:
        hex: A hexadecimal color value.
            Format:

                - :py:`"^hex_[0-9,a-f]{6}$"` (e.g. :py:`"hex_ffffff"`)

        colormode: Just provided for compatibility but is ignored since
            hexdecimalcolor value toogles colormode 256 automatically.
    """
    key = parse_hex(hex)
    return get_color_id_from_color_enum(key, Colors256), 256


def get_color_id_from_color_value(color_value: t.ColorValue,
                                  colormode: int) -> t.Tuple[str, int]:
    """Returns a color id and the correct colormode.

    Iterarble (eg. :py:`(255, 0, 0)` are parsed into valid key format (eg.
    :py:`"rgb_255_0_0"`) before lookup. See :func:`.parse_color_value` for
    details.

    Args:
        color_value: A color value as :py:`list` or :py:`tuple` with
            :py:`len(color_value) == 3`

        colormode: Just provided for compatibility but is ignored since rgb/hsl
            color values toogle colormode 256 automatically.
    """
    key = parse_color_value(color_value)
    return get_color_id_from_color_enum(key, Colors256)


def get_color_string(color_id: str, colormode: int) -> str:
    """Return get_color_string func for colormode."""
    switcher = {8: get_color_string_8_bit,
                16: get_color_string_16_bit,
                256: get_color_string_256_bit
                }
    return switcher[colormode](color_id)


def get_color_string_256_bit(color_id: str) -> str:
    """Return ANSI color command string for 256 bit colors"""
    return Colors._blink + ANSICommands.separator + \
        TextAttributes.blink + ANSICommands.separator + color_id


def get_color_string_16_bit(color_id: str) -> str:
    """Return ANSI color command string for 16 bit (bold) colors"""
    return color_id + ANSICommands.separator + TextAttributes.bold


def get_color_string_8_bit(color_id: str) -> str:
    """Return ANSI color command string for 8 bit colors"""
    return color_id


#--------------------- Checker ------------------------------
def any_is_not_none(*args: t.Any) -> bool:
    return any(arg is not None for arg in args)


def all_are_none(*args: t.Any) -> bool:
    return all(arg is None for arg in args)


def any_is_none(*args: t.Any) -> bool:
    return any(arg is None for arg in args)


def all_are_not_none(*args: t.Any) -> bool:
    return all(arg is not None for arg in args)


def is_8bit_color(name: str) -> bool:
    """Return True if name is a valid key of Colors-Enum."""
    return name in Colors.__members__.keys()


def is_valid_hex_string(hex: str) -> bool:
    """Return True if hex is a valid hexadecimal color value string."""
    return (hex.startswith("#") and len(hex) ==
            7 and has_only_valid_characters(hex))


def has_only_valid_characters(hex: str) -> bool:
    """Return True if hex has only valid hexadecimal characters."""
    _valid_hex_characters = set("#abcdef0123456789")
    return set(hex) <= _valid_hex_characters


if __name__ == '__main__':
    import doctest
    doctest.testmod()
