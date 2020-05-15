# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EVENTS
Menu events definition and locals.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2020 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

import pygame.locals as __locals


class MenuAction(object):
    """
    Pymenu events.

    :param action: Action identifier
    :type action: int
    """

    def __init__(self, action):
        assert isinstance(action, int)
        self._action = action

    def __eq__(self, other):
        if isinstance(other, MenuAction):
            return self._action == other._action
        return False


# Events
BACK = MenuAction(0)  # Menu back
CLOSE = MenuAction(1)  # Close menu
DISABLE_CLOSE = MenuAction(2)  # Menu disable closing
EXIT = MenuAction(3)  # Menu exit program
NONE = MenuAction(4)  # None action
RESET = MenuAction(5)  # Menu reset

# Pygame events
PYGAME_QUIT = __locals.QUIT
