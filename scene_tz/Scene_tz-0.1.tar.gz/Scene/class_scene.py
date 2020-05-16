# coding=utf-8
import time

import graphics as gr
from Scene.base_scene import BaseScene
from graphics import color_rgb


class Scene(BaseScene):
    _img = None  # type: gr.GraphWin
    _color = 'black'

    def __init__(self, width, height, bg='black'):
        super().__init__(width, height, bg)

        self._img = gr.GraphWin("Jenkslex and Ganzz project", self.width, self.height)
        self._img.setBackground(self._bg)

    # def imagettftext2
    # def _imagettftext
    # def _imagestring

    def set_char(self, x, y, c, size):
        t = gr.Text(gr.Point((x + 0.5) * size, (y + 0.5) * size), c)
        t.setFill(self._color)
        t.draw(self._img)

    def get_pixel(self, x, y):
        return self._img.getPixel(x, y)

    def get_color(self, r, g, b):
        # type: (int, int, int) -> str
        return color_rgb(r, g, b)

    def line(self, x1, y1, x2, y2, color):
        # type: (int, int, int, int, str) -> Scene
        line = gr.Line(gr.Point(x1, y1), gr.Point(x2, y2))
        line.setOutline(color)
        line.draw(self._img)
        return self

    # обратная система координат

    def line_inv(self, x1, y1, x2, y2, color):
        # type: (int, int, int, int, str) -> Scene
        return self.line(x1, self.height - y1, x2, self.height - y2, color)

    def poly_lines(self, color, points):
        # type: (str, [[2]]) -> Scene
        first = points.pop(0)

        last = first

        for next_point in points:
            self.line(last[0], last[1], next_point[0], next_point[1], color)
            last = next_point

        if self.closed:
            self.line(last[0], last[1], first[0], first[1], color)

        return self

    def oval_spin(self, _cx, _cy, _r1, _r2, u, _color):
        # type: (int, int, int, int, int, str) -> Scene
        return self.arc(_cx, _cy, _r1, _r2, _color, 0, 360, u)

    def circle(self, _cx, _cy, _r, _color, poly_lines=False):
        # type: (int, int, int, str) -> Scene
        if poly_lines:
            return self.arc(_cx, _cy, _r, _r, _color, 0, 360)
        c = gr.Circle(gr.Point(_cx, _cy), _r)
        c.setOutline(_color)
        c.draw(self._img)
        return self

    def clear(self):
        # type: () -> Scene
        self._img.delete("all")
        return self

    def draw(self):
        # type: () -> Scene
        while not self._img.isClosed():
            time.sleep(.1)  # give up thread
            self.clear().redraw()
            # self._img.getMouse()
        self._img.close()
        return self

    def redraw(self):
        # type: () -> Scene
        return self
