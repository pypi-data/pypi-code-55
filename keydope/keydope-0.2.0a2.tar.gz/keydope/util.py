import logging
import subprocess
import time

import Xlib.display
from Xlib.display import error as xlib_error

logger = logging.getLogger(__name__)

# Calling Xlib.display.Display() in each function invocation has a runtime
# impact and also leaks memory, so we cache the default display in a global
# variable.
# pylint: disable=invalid-name
_default_display = None


def get_default_display():
    # pylint: disable=global-statement
    global _default_display
    if _default_display is None:
        _default_display = Xlib.display.Display()
    return _default_display


XLIB_EXCEPTIONS = (
    xlib_error.DisplayError,
    xlib_error.XError,
    xlib_error.ConnectionClosedError,
    xlib_error.XauthError,
    xlib_error.XNoAuthError,
    xlib_error.ResourceIDError,
)


class RescueRequested(Exception):
    pass


class WindowMetadata:

    def __init__(self, window_class=None, window_instance=None, title=None):
        self.window_class = window_class
        self.window_instance = window_instance
        self.title = title


def _get_active_window(display=None):
    try:
        if display is None:
            display = get_default_display()
        input_focus = display.get_input_focus()
    except XLIB_EXCEPTIONS as e:
        raise OSError(
            'Can\'t get active window, error from xlib/X11: {}'.format(e))
    # get_input_focus sometimes returns an integer in the focus field. I would
    # expect this to raise an exception, but since it doesn't we check it.
    if not hasattr(input_focus.focus, 'get_wm_name'):
        raise OSError('X11 returned bad object for focused window: {}'.format(
            input_focus))
    return input_focus.focus


def get_active_window_metadata(display=None):
    window = _get_active_window(display)
    try:
        wm_instance_class = window.get_wm_class()
        title = window.get_wm_name()
    except XLIB_EXCEPTIONS as e:
        raise OSError(
            'Can\'t extract window metadata, error from xlib/X11: {}'.format(e))
    if not wm_instance_class:
        return WindowMetadata(title=title)
    return WindowMetadata(wm_instance_class[1], wm_instance_class[0], title)


# def get_class_name(window):
#     """Get window's class name (recursively checks parents)"""
#     try:
#         wmname = window.get_wm_name()
#         wmclass = window.get_wm_class()
#         # workaround for Java app
#         # https://github.com/JetBrains/jdk8u_jdk/blob/316948b6cfb8e8fbb722512b34f324cd3be1a894/src/solaris/classes/sun/awt/X11/XFocusProxyWindow.java#L35
#         if (wmclass is None and wmname is None) or "FocusProxy" in wmclass:
#             parent_window = window.query_tree().parent
#             if parent_window:
#                 return get_class_name(parent_window)
#             return None
#         return wmclass
#     except:
#         return None
