import time

import svgwrite

from Scene.base_scene import BaseScene

cm_to_point = 28.3464566929  # in swf
cm_to_pixel = 37.7952755906  # in web


class Scene(BaseScene):
    _img = None  # type: svgwrite.Drawing
    _color = 'black'

    def __init__(self, width, height, bg='black'):
        super().__init__(width, height, bg)

        self._img = svgwrite.Drawing(debug=True, size=(self.width, self.height), profile='tiny')
        # self._img.viewbox(0, 0, self.width*10, self.height*10)
        # self._img.
        # checkerboard has a size of 10cm x 10cm;
        # defining a viewbox with the size of 80x80 means, that a length of 1
        # is 10cm/80 == 0.125cm (which is for now the famous USER UNIT)
        # but I don't have to care about it, I just draw 8x8 squares, each 10x10 USER-UNITS
        # self._img.setBackground(self._bg)

    def get_pixel(self, x, y):
        return self._img.getPixel(x, y)

    def get_color(self, r, g, b):
        # type: (float, float, float) -> str
        return svgwrite.rgb(r, g, b, '%')

    def line(self, x1, y1, x2, y2, color):
        # type: (float, float, float, float, str) -> Scene

        line = self._img.line(start=(x1, y1), end=(x2, y2), stroke=color)  # type : shapes.Line
        self._img.add(line)

        return self

        # обратная система координат

    def line_inv(self, x1, y1, x2, y2, color):
        # type: (float, float, float, float, [int, int, int]) -> Scene
        return self.line(x1, self.height - y1, x2, self.height - y2, color)

    def poly_lines(self, color, points):
        # type: (str, [int, int]) -> Scene
        if self.closed:
            polygon = self._img.polygon(points, stroke=color, fill='none')  # type : shapes.Polygon
            self._img.add(polygon)
        else:
            polyline = self._img.polyline(points, stroke=color, fill='none')  # type : shapes.Polyline
            self._img.add(polyline)

        return self

    def oval_spin(self, _cx, _cy, _r1, _r2, u, _color):
        # type: (int, int, int, int, int, [int, int, int]) -> Scene
        return self.arc(_cx, _cy, _r1, _r2, _color, 0, 360, u)

    def circle(self, _cx, _cy, _r, _color, poly_lines=False):
        # type: (float, float, float, str, bool) -> Scene

        if poly_lines:
            return self.arc(_cx, _cy, _r, _r, _color, 0, 360)

        circle = self._img.circle(center=(_cx, _cy), r=_r, stroke=_color, stroke_width=1, fill="none")
        self._img.add(circle)

        return self

    '''
    def arc(self, _cx, _cy, _r1, _r2, _color, _a, _arc, u=0):
        # type: (int, int, int, int, str, int, int, int) -> Scene

        if _arc == 360:
            ellipse = self._img.add(self._img.ellipse(center=(_cx, _cy), r=(_r1, _r2)))  # type : shapes.Ellipse
            ellipse.fill('none').stroke(_color, width=1)#.dasharray([20, 20])
        else:

            alfastart = math.radians(_a)
            alfaend = math.radians(_arc - _a)

            start_x, start_y = self.getacrpoint(_r1, _r2, alfastart, u)  # + [_cx, _cy]
            end_x, end_y = self.getacrpoint(_r1, _r2, alfaend, u)

            #self.line(start_x + _cx, start_y + _cy, end_x + _cx, end_y + _cy, _color)

            largeArcFlag = {True: "1", False: "0"}[alfaend - alfastart <= 180]

            args = {'x0': start_x + _cx,
                    'y0': start_y + _cy,
                    'xradius': _r1,
                    'yradius': _r2,
                    'largeArcFlag': largeArcFlag,
                    'ellipseRotation': 0,  # has no effect for circles
                    'x1': end_x + _cx,
                    'y1': end_y + _cy}
            self._img.add(
                self._img.path(
                    d="M %(x0)f,%(y0)f A %(xradius)f,%(yradius)f %(ellipseRotation)f %(largeArcFlag)s,0 %(x1)f,%(y1)f" % args,
                    fill="none",
                    stroke=_color, stroke_width=1
                    ))

        return self
'''

    def redraw(self):
        pass

    def draw(self, name=None):
        self.redraw()
        if name is None:
            name = time.strftime("%Y%m%d-%H%M%S.svg")
        self._img.saveas(filename=name)
        return name
