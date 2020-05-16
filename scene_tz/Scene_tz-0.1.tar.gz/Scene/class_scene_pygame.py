# coding=utf-8
# Import a library of functions called 'pygame'
import math

import pygame

from Scene.base_scene import BaseScene

# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Scene(BaseScene):
    _img = None  # type: pygame.Surface
    _color = BLACK

    def __init__(self, width, height, bg=BLACK):
        super().__init__(width, height, bg)

        # Set the height and width of the screen
        size = (self.width, self.height)
        self._img = pygame.display.set_mode(size)

        pygame.display.set_caption("Jenkslex and Ganzz project")

        self._img.fill(self._bg)

        # Loop until the user clicks the close button.
        self.done = False
        self.clock = pygame.time.Clock()

    # def imagettftext2
    # def _imagettftext
    # def _imagestring

    def get_pixel(self, x, y):
        return self._img.getPixel(x, y)

    def get_color(self, r, g, b):
        # type: (int, int, int) -> [int, int, int]
        return r, g, b

    def line(self, x1, y1, x2, y2, color):
        # type: (int, int, int, int, [int, int, int]) -> Scene
        pygame.draw.line(self._img, color, [x1, y1], [x2, y2], 1)
        return self

    # обратная система координат

    def line_inv(self, x1, y1, x2, y2, color):
        # type: (int, int, int, int, [int, int, int]) -> Scene
        return self.line(x1, self.height - y1, x2, self.height - y2, color)

    def poly_lines(self, color, points):
        # type: (str, [int, int]) -> Scene
        pygame.draw.lines(self._img, color, self.closed, points)

        return self

    def oval_spin(self, _cx, _cy, _r1, _r2, u, _color):
        # type: (int, int, int, int, int, [int, int, int]) -> Scene
        return self.arc(_cx, _cy, _r1, _r2, _color, 0, 360, u)

    def circle(self, _cx, _cy, _r, _color, poly_lines=False):
        # type: (int, int, int, str) -> Scene
        if poly_lines:
            return self.arc(_cx, _cy, _r, _r, _color, 0, 360)
        pygame.draw.arc(self._img, _color, [_cx - _r, _cy - _r, 2 * _r, 2 * _r], 0, math.pi * 2)
        return self

    def clear(self):
        # type: () -> Scene
        # Clear the screen and set the screen background
        self._img.fill(self._bg)
        return self

    def draw(self):
        # type: () -> Scene
        # Loop as long as done == False
        while not self.done:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.done = True  # Flag that we are done so we exit this loop

            # All drawing code happens after the for loop and but
            # inside the main while not done loop.

            self.clear().redraw()

            # Go ahead and update the screen with what we've drawn.
            # This MUST happen after all the other drawing commands.
            pygame.display.flip()

            # This limits the while loop to a max of 60 times per second.
            # Leave this out and we will use all CPU we can.
            self.clock.tick(60)

    def redraw(self):
        # type: () -> Scene
        return self

    def text(self, textsurface, place):
        return self._img.blit(textsurface, place)


# Be IDLE friendly
pygame.quit()
