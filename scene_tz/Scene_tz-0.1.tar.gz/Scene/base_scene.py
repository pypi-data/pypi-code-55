import math
from typing import Any


class MathGeometry:
    @staticmethod
    def get_acr_point(_r1, _r2, _a, u=0):
        # type: (float, float, float, float) -> [int, int]
        a0 = _a

        x = _r1 * math.cos(a0)
        y = _r2 * math.sin(a0)

        alfa = math.radians(u)
        sina = math.sin(alfa)
        cosa = math.cos(alfa)

        tmpx = x * cosa - y * sina
        tmpy = x * sina + y * cosa

        x = tmpx
        y = tmpy

        return x, y

    def get_rad_step(self, r):
        # type: (int) -> int
        if r <= 10:
            return r
        if self.Data_value[r - 11] == 0:
            self.calc_rad_step(r)

        return self.Data_value[r - 11]

    Data_value = [0] * 1000

    def calc_rad_step(self, r):
        # type: (int) -> None
        n = r
        while n <= r:
            i = 1
            if n < i:
                n = r
            while i <= n:
                rrr = math.sqrt(
                    r * (
                            pow(math.cos(0 + math.pi / i) - math.cos(0), 2) +
                            pow(math.sin(0 + math.pi / i) - math.sin(0), 2)
                    )
                )
                if rrr <= 1:
                    self.Data_value[r - 11] = i
                    return
                i += 1
            n += 1

    @staticmethod
    def calc_intersection_line_line(line1, line2):
        x1_1, y1_1, x1_2, y1_2 = line1
        x2_1, y2_1, x2_2, y2_2 = line2

        xx = [x1_1, x1_2]
        min_xx_1 = min(xx)
        max_xx_1 = max(xx)

        yy = [y1_1, y1_2]
        min_yy_1 = min(yy)
        max_yy_1 = max(yy)

        xx = [x2_1, x2_2]
        min_xx_2 = min(xx)
        max_xx_2 = max(xx)

        yy = [y2_1, y2_2]
        min_yy_2 = min(yy)
        max_yy_2 = max(yy)

        if min_xx_1 > max_xx_2 or max_xx_1 < min_xx_2:
            return []

        A1 = y1_1 - y1_2
        B1 = x1_2 - x1_1
        C1 = x1_1 * y1_2 - x1_2 * y1_1
        A2 = y2_1 - y2_2
        B2 = x2_2 - x2_1
        C2 = x2_1 * y2_2 - x2_2 * y2_1

        if B1 * A2 - B2 * A1 and A1:
            y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
            x = (-C1 - B1 * y) / A1
            if (min_xx_1 <= x <= max_xx_1 and min_yy_1 <= y <= max_yy_1) and (
                    min_xx_2 <= x <= max_xx_2 and min_yy_2 <= y <= max_yy_2):
                return [x, y]
        elif B1 * A2 - B2 * A1 and A2:
            y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
            x = (-C2 - B2 * y) / A2
            if (min_xx_1 <= x <= max_xx_1 and min_yy_1 <= y <= max_yy_1) and (
                    min_xx_2 <= x <= max_xx_2 and min_yy_2 <= y <= max_yy_2):
                return [x, y]

        return []

    def calc_intersection_ellipse_line(self, ellipse, line):
        # точка пересечения линии и эллипса
        # [] если нет либо точка [x, y]
        cx, cy, r1, r2, u, alfastart, alfaend = ellipse
        x1, y1, x2, y2 = line

        last = []

        a0 = alfaend
        while a0 >= 0:
            x, y = self.get_acr_point(r1, r2, alfastart - a0, u)

            point = [cx + x, cy + y]
            if len(last):
                result = self.calc_intersection_line_line([point[0], point[1], last[0], last[1]], [x1, y1, x2, y2])
                if len(result) > 0:
                    return result
            last = point
            rrr = math.fabs(x) + math.fabs(y)

            da = math.pi / self.get_rad_step(math.trunc(rrr) + 1)
            a0 -= da
        x, y = self.get_acr_point(r1, r2, alfastart, u)

        point = [cx + x, cy + y]
        result = self.calc_intersection_line_line([point[0], point[1], last[0], last[1]], [x1, y1, x2, y2])
        if len(result) > 0:
            return result

        return []

    def calc_intersection_ellipse_ellipse(self, ellipse1, ellipse2):
        # точка пересечения эллипса и эллипса
        # [] если нет либо точка [x, y]
        cx, cy, r1, r2, u, alfastart, alfaend = ellipse1

        last = []

        a0 = alfaend
        while a0 >= 0:
            x, y = self.get_acr_point(r1, r2, alfastart - a0, u)

            point = [cx + x, cy + y]
            if len(last):
                result = self.calc_intersection_ellipse_line(ellipse2, [point[0], point[1], last[0], last[1]])
                if len(result) > 0:
                    return result
            last = point
            rrr = math.fabs(x) + math.fabs(y)

            da = math.pi / self.get_rad_step(math.trunc(rrr) + 1)
            a0 -= da
        x, y = self.get_acr_point(r1, r2, alfastart, u)

        point = [cx + x, cy + y]
        result = self.calc_intersection_ellipse_line(ellipse2, [point[0], point[1], last[0], last[1]])
        if len(result) > 0:
            return result

        return []


# базовые функции сцены зависящие от конечной реализации
class BaseSceneClass:
    def __init__(self, width, height, bg='black'):
        self.width = width
        self.height = height

        self._bg = bg

    def get_pixel(self, x, y):
        # type: (float, float) -> BaseSceneClass
        """

        :param x: float
        :param y: float
        :return: BaseSceneClass
        """
        return self

    def get_color(self, r, g, b):
        # type: (float, float, float) -> Any
        """

        :param r: float
        :param g: float
        :param b: float
        :return: Any
        """
        return ''

    def line(self, x1, y1, x2, y2, color):
        # type: (float, float, float, float, str) -> BaseSceneClass
        """

        :param x1: float
        :param y1: float
        :param x2: float
        :param y2: float
        :param color: Any
        :return: BaseSceneClass
        """
        return self

    def line_inv(self, x1, y1, x2, y2, color):
        # type: (float, float, float, float, Any) -> BaseSceneClass
        """
        обратная система координат

        :param x1: float
        :param y1: float
        :param x2: float
        :param y2: float
        :param color: Any
        :return: BaseSceneClass
        """
        return self

    def circle(self, _cx, _cy, _r, _color, poly_lines=False):
        return self

    def poly_lines(self, color, points):
        return self

    def oval_spin(self, _cx, _cy, _r1, _r2, u, _color):
        return self


# графические примитивы
class GraphicsItems(BaseSceneClass, MathGeometry):
    def rectangle(self, x1, y1, x2, y2, color):
        return self.poly_lines(color, [[x1, y1], [x1, y2], [x2, y2], [x2, y1]])

    def arc(self, _cx, _cy, _r1, _r2, _color, _a, _arc, u=0):
        # type: (float, float, float, float, str, float, float, float) -> GraphicsItems
        points = []
        alfastart = math.radians(_a)
        alfaend = math.radians(_arc)

        a0 = alfaend
        while a0 >= 0:
            x, y = self.get_acr_point(_r1, _r2, alfastart - a0, u)

            points.append([_cx + x, _cy + y])

            rrr = math.fabs(x) + math.fabs(y)

            # self.setpixel(_cx + x, _cy + y, _color)
            # self.circle(_cx + x, _cy + y, 3, _color)

            da = math.pi / self.get_rad_step(math.trunc(rrr) + 1)
            a0 -= da

        x, y = self.get_acr_point(_r1, _r2, alfastart, u)

        points.append([_cx + x, _cy + y])

        self.poly_lines(_color, points)
        return self

    def ellipse(self, _cx, _cy, _r1, _r2, _color, u=0):
        return self.arc(_cx, _cy, _r1, _r2, _color, 0, 360, u)

    def set_pixel(self, _x, _y, _color):
        # type: (float, float, Any) -> GraphicsItems
        self.line(_x, _y, _x, _y, _color)
        return self


class ColorStack(GraphicsItems):
    _color = 'black'
    _colors = []

    def c_pop_color(self):
        # type: () -> ColorStack
        (self._color) = self._colors.pop()
        return self

    def c_push_color(self):
        # type: () -> ColorStack
        self._colors.append(self._color)
        return self

    def c_step_color(self, _r, _g, _b):
        # type: (int, int, int) -> ColorStack
        return self \
            .c_push_color() \
            .c_set_color(_r, _g, _b)

    # связанные с родителями
    def c_set_color(self, _r, _g, _b):
        # type: (int, int, int) -> ColorStack
        self._color = self.get_color(_r, _g, _b)
        return self


# системы dx dy
class IncrementMove(ColorStack):
    _x = 0
    _y = 0
    _steps = []

    def i_pop_step(self):
        # type: () -> IncrementMove
        (self._x, self._y) = self._steps.pop()
        return self

    def i_push_step(self):
        # type: () -> IncrementMove
        self._steps.append([self._x, self._y])
        return self

    def i_move_to(self, x, y):
        # type: (float, float) -> IncrementMove
        self._x = x
        self._y = y
        return self

    def i_step(self, dx, dy):
        # type: (float, float) -> IncrementMove
        return self \
            .i_push_step() \
            .i_move_to(self._x + dx, self._y + dy)

    # связанные с родителями
    def i_set_pixel(self):
        # type: () -> IncrementMove
        return self \
            .set_pixel(self._x, self._y, self._color)

    def i_line_to(self, x, y):
        # type: (float, float) -> IncrementMove
        return self \
            .line(self._x, self._y, x, y, self._color) \
            .i_move_to(x, y)

    # обратная система координат
    def i_line_to_inv(self, x, y):
        # type: (float, float) -> IncrementMove
        return self \
            .line(self._x, self.height - self._y, x, self.height - y, self._color) \
            .i_move_to(x, y)

    def i_line_step(self, x, y):
        # type: (float, float) -> IncrementMove
        return self \
            .line(self._x, self._y, self._x + x, self._y + y, self._color) \
            .i_move_to(self._x + x, self._y + y)

    def i_line_and_step(self, x, y):
        # type: (float, float) -> IncrementMove
        return self \
            .line(self._x, self._y, self._x + x, self._y + y, self._color) \
            .i_step(x, y)

    def i_circle(self, _r, polylines=False):
        # type: (float, bool) -> IncrementMove
        return self \
            .circle(self._x, self._y, _r, self._color, polylines)

    def i_arc(self, _r1, _r2, _a, _arc):
        # type: (int, int, int, int) -> IncrementMove
        return self \
            .arc(self._x, self._y, _r1, _r2, self._color, _a, _arc)

    def i_center(self):
        # type: () -> IncrementMove
        return self \
            .i_move_to(self.width / 2, self.height / 2)

    def lines(self):
        # type: () -> IncrementMove
        """
        рисуем линии координат
        :return: IncrementMove
        """

        cx = self.width / 2  # центр по х
        cy = self.height / 2  # центр по у
        return self \
            .c_set_color(0, 255, 0).i_move_to(cx, 0).i_line_step(0, self.height).i_move_to(0, cy).i_line_step(
            self.width, 0)


class DigitalOutputScene(IncrementMove):
    _size = 5
    _sizes = []

    def d_pop_digital_size(self):
        # type: () -> DigitalOutputScene
        self._size = self._sizes.pop()
        return self

    def d_push_digital_size(self):
        # type: () -> DigitalOutputScene
        self._sizes.append(self._size)
        return self

    def d_set_digital_size(self, size):
        # type: (int) -> DigitalOutputScene
        self._size = size

        return self

    def _draw_digital(self, elem):
        # type: ([int]) -> DigitalOutputScene

        for ndx, member in enumerate(elem):
            if member == 1:
                self.i_step(0, 0).i_line_step(self._size, 0).i_pop_step()
            elif member == 2:
                self.i_step(self._size, 0).i_line_step(self._size, 0).i_pop_step()
            elif member == 3:
                self.i_step(self._size * 2, 0).i_line_step(self._size, 0).i_pop_step()
            elif member == 4:
                self.i_step(self._size * 3, 0).i_line_step(self._size, 0).i_pop_step()
            elif member == 5:
                self.i_step(0, self._size * 4).i_line_step(self._size, 0).i_pop_step()
            elif member == 6:
                self.i_step(self._size, self._size * 4).i_line_step(self._size, 0).i_pop_step()
            elif member == 7:
                self.i_step(self._size * 2, self._size * 4).i_line_step(self._size, 0).i_pop_step()
            elif member == 8:
                self.i_step(self._size * 3, self._size * 4).i_line_step(self._size, 0).i_pop_step()
            elif member == 9:
                self.i_step(0, self._size * 8).i_line_step(self._size, 0).i_pop_step()
            elif member == 10:
                self.i_step(self._size, self._size * 8).i_line_step(self._size, 0).i_pop_step()
            elif member == 11:
                self.i_step(self._size * 2, self._size * 8).i_line_step(self._size, 0).i_pop_step()
            elif member == 12:
                self.i_step(self._size * 3, self._size * 8).i_line_step(self._size, 0).i_pop_step()
            elif member == 13:
                self.i_step(0, 0).i_line_step(0, self._size).i_pop_step()
            elif member == 14:
                self.i_step(0, self._size).i_line_step(0, self._size).i_pop_step()
            elif member == 15:
                self.i_step(0, self._size * 2).i_line_step(0, self._size).i_pop_step()
            elif member == 16:
                self.i_step(0, self._size * 3).i_line_step(0, self._size).i_pop_step()
            elif member == 17:
                self.i_step(0, self._size * 4).i_line_step(0, self._size).i_pop_step()
            elif member == 18:
                self.i_step(0, self._size * 5).i_line_step(0, self._size).i_pop_step()
            elif member == 19:
                self.i_step(0, self._size * 6).i_line_step(0, self._size).i_pop_step()
            elif member == 20:
                self.i_step(0, self._size * 7).i_line_step(0, self._size).i_pop_step()
            elif member == 21:
                self.i_step(self._size * 4, 0).i_line_step(0, self._size).i_pop_step()
            elif member == 22:
                self.i_step(self._size * 4, self._size).i_line_step(0, self._size).i_pop_step()
            elif member == 23:
                self.i_step(self._size * 4, self._size * 2).i_line_step(0, self._size).i_pop_step()
            elif member == 24:
                self.i_step(self._size * 4, self._size * 3).i_line_step(0, self._size).i_pop_step()
            elif member == 25:
                self.i_step(self._size * 4, self._size * 4).i_line_step(0, self._size).i_pop_step()
            elif member == 26:
                self.i_step(self._size * 4, self._size * 5).i_line_step(0, self._size).i_pop_step()
            elif member == 27:
                self.i_step(self._size * 4, self._size * 6).i_line_step(0, self._size).i_pop_step()
            elif member == 28:
                self.i_step(self._size * 4, self._size * 7).i_line_step(0, self._size).i_pop_step()
            elif member == 29:
                self.i_step(0, self._size).i_line_step(self._size, -self._size).i_pop_step()
            elif member == 30:
                self.i_step(0, self._size * 5).i_line_step(self._size, -self._size).i_pop_step()
            elif member == 31:
                self.i_step(self._size * 3, self._size * 4).i_line_step(self._size, -self._size).i_pop_step()
            elif member == 32:
                self.i_step(self._size * 3, self._size * 8).i_line_step(self._size, -self._size).i_pop_step()
            elif member == 33:
                self.i_step(self._size * 3, self._size * 0).i_line_step(self._size, self._size).i_pop_step()
            elif member == 34:
                self.i_step(self._size * 0, self._size * 3).i_line_step(self._size, self._size).i_pop_step()
            elif member == 35:
                self.i_step(self._size * 0, self._size * 7).i_line_step(self._size, self._size).i_pop_step()
            elif member == 36:
                self.i_step(self._size * 3, self._size * 4).i_line_step(self._size, self._size).i_pop_step()
            elif member == 37:
                self.i_step(self._size * 2, self._size * 0).i_line_step(-2 * self._size, 4 * self._size).i_pop_step()
            elif member == 38:
                self.i_step(self._size * 4, self._size * 0).i_line_step(-2 * self._size, 4 * self._size).i_pop_step()
            elif member == 39:
                self.i_step(self._size * 2, self._size * 0).i_line_step(0, 4 * self._size).i_pop_step()
            elif member == 40:
                self.i_step(self._size * 2, self._size * 4).i_line_step(0, 4 * self._size).i_pop_step()
            elif member == 41:
                self.i_step(self._size * 2, self._size * 4).i_line_step(-2 * self._size, 4 * self._size).i_pop_step()
            elif member == 42:
                self.i_step(self._size * 4, self._size * 4).i_line_step(-2 * self._size, 4 * self._size).i_pop_step()
            elif member == 43:
                self.i_step(self._size * 0, self._size * 0).i_line_step(2 * self._size, 4 * self._size).i_pop_step()
            elif member == 44:
                self.i_step(self._size * 2, self._size * 0).i_line_step(2 * self._size, 4 * self._size).i_pop_step()
            elif member == 45:
                self.i_step(self._size * 0, self._size * 4).i_line_step(2 * self._size, 4 * self._size).i_pop_step()
            elif member == 46:
                self.i_step(self._size * 2, self._size * 4).i_line_step(2 * self._size, 4 * self._size).i_pop_step()

        return self.i_step(self._size * 5, 0)

    def d_draw_tex(self, string, center=False):
        # type: (str, bool) -> DigitalOutputScene
        length = len(string)
        if center:
            self.i_step(-self._size * 2 * length, -self._size * 4)
        for x in string:
            self.d_out_char(x)
        for _ in string:
            self.i_pop_step()
        return self.i_pop_step()

    def d_out_char(self, in_char):
        # type: (str) -> DigitalOutputScene
        char = in_char.upper()
        '''
        1- 2- 3- 4-
        5- 6- 7- 8- 
        9- 10- 11- 12-
        
        13-20 | 21-28 |
        
        '''
        # todo рисовать примитивами - дугами окружностями
        data = {
            ' ': [],
            '-': [6, 7],
            ':': [30, 31, 34, 36, ],
            '-1': [x for x in range(47)],
            '0': [1, 2, 3, 33, 22, 23, 24, 25, 26, 27, 28, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 35],
            '1': [39, 40, 11, 10, 37],
            '2': [1, 2, 3, 6, 7, 8, 9, 10, 11, 33, 30, 32, 13, 22, 23, 24, 18, 19, 20, 27],
            '3': [1, 2, 3, 6, 7, 8, 9, 10, 11, 33, 32, 13, 22, 23, 24, 20, 27, 26, 25],
            '4': [13, 14, 15, 22, 23, 24, 25, 26, 27, 28, 6, 7, 8, 33, 34],
            '5': [2, 3, 4, 5, 6, 7, 10, 11, 12, 29, 36, 35, 14, 15, 16, 19, 21, 26, 27, 28],
            '6': [1, 2, 3, 6, 7, 10, 11, 12, 33, 5, 36, 35, 13, 14, 15, 16, 17, 18, 19, 28, 27, 26],
            '7': [38, 40, 2, 3, 4, 29, 14, 10, 11],
            '8': [1, 2, 3, 33, 22, 23, 24, 25, 26, 27, 28, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 35, 5, 6, 7, 8],
            '9': [1, 2, 3, 33, 22, 23, 24, 25, 26, 27, 28, 10, 11, 12, 13, 14, 15, 19, 35, 34, 6, 7, 8],

            'A': [2, 3, 5, 6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 33],
            'B': [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 26, 27, 31, 32, 33, 36],
            'C': [1, 2, 3, 33, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 35],
            'D': [1, 2, 3, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 32, 33, ],
            'E': [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20],
            'F': [1, 2, 3, 5, 6, 7, 13, 14, 15, 16, 17, 18, 19, 20],
            'G': [1, 2, 3, 8, 33, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 25, 26, 27, 28, 35],
            'H': [5, 6, 7, 8, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
            'I': [1, 2, 3, 4, 9, 10, 11, 12, 39, 40],
            'J': [3, 4, 10, 11, 12, 21, 22, 23, 24, 25, 26, 27, 28, 35],
            'K': [5, 6, 13, 14, 15, 16, 17, 18, 19, 20, 38, 46],
            'L': [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            'M': [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 38, 43],
            'N': [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 43, 46],
            'O': [1, 2, 3, 33, 22, 23, 24, 25, 26, 27, 28, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 35],
            'P': [1, 2, 3, 5, 6, 7, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 31, 33],
            'Q': [1, 2, 3, 33, 22, 23, 24, 25, 26, 27, 28, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 35, 46],
            'R': [1, 2, 3, 5, 6, 7, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 31, 33, 46],
            'S': [1, 2, 3, 5, 6, 7, 8, 33, 25, 26, 27, 28, 10, 11, 12, 13, 14, 15, 16, 35],
            'T': [1, 2, 3, 4, 39, 40],
            'U': [10, 11, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26, 27, 32, 35],
            'V': [13, 14, 15, 16, 21, 22, 23, 24, 42, 45],
            'W': [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 41, 46],
            'X': [38, 41, 43, 46],
            'Y': [38, 40, 43],
            'Z': [1, 2, 3, 4, 9, 10, 11, 12, 38, 41],

            'А': [2, 3, 5, 6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 33],
            'Б': [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 26, 27, 32, 36],
            'В': [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 26, 27, 31, 32, 33, 36],
            'Г': [1, 2, 3, 13, 14, 15, 16, 17, 18, 19, 20],
            'Д': [1, 2, 3, 5, 6, 7, 8, 10, 11, 17, 18, 19, 22, 23, 24, 25, 26, 27, 32, 33, 35, ],
            'Е': [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20],
            'Ё': [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 29],
            'Ж': [38, 39, 40, 41, 43, 46],
            'З': [2, 3, 5, 6, 7, 10, 11, 22, 23, 26, 27, 29, 31, 32, 33, 35, 36],
            'И': [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 38, 41],
            'Й': [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 38, 41],
            'К': [5, 6, 13, 14, 15, 16, 17, 18, 19, 20, 38, 46],
            'Л': [3, 4, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 37],
            'М': [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 38, 43],
            'Н': [5, 6, 7, 8, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
            'О': [1, 2, 3, 33, 22, 23, 24, 25, 26, 27, 28, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 35],
            'П': [1, 2, 3, 4, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
            'Р': [1, 2, 3, 5, 6, 7, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 31, 33],
            'С': [1, 2, 3, 33, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 35],
            'Т': [1, 2, 3, 4, 39, 40],
            'У': [38, 41, 43],
            'Ф': [2, 3, 6, 7, 14, 15, 22, 23, 29, 31, 33, 34, 39, 40],
            'Х': [38, 41, 43, 46],
            'Ц': [9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 21, 22, 23, 24, 25, 26, 27, 32, 46],
            'Ч': [6, 7, 8, 13, 14, 15, 21, 22, 23, 24, 25, 26, 27, 28, 34],
            'Ш': [9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 32, 39, 40],
            'Щ': [9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 32, 39, 40, 46],
            'Ъ': [1, 2, 7, 11, 26, 27, 32, 36, 39, 40],
            'Ы': [5, 6, 9, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 32, 40],
            'Ь': [13, 14, 15, 16, 17, 18, 19, 20, 26, 27, 5, 6, 7, 9, 10, 11, 32, 36],
            'Э': [2, 3, 4, 6, 7, 8, 10, 11, 12, 21, 22, 23, 24, 25, 26, 27, 28, 29, 35],
            'Ю': [3, 5, 6, 11, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 39, 40, 32, 33],
            'Я': [2, 3, 4, 6, 7, 8, 14, 15, 21, 22, 23, 24, 25, 26, 27, 28, 29, 34, 41],
        }

        if char in data:
            return self._draw_digital(data[char])

        return self._draw_digital(data['-1'])


class BaseScene(DigitalOutputScene):
    closed = True

    def set_closed(self, value):
        # type: (bool) -> BaseScene
        self.closed = value
        return self

    # todo
    # def fill
    # def fillarc
    # def fillcircle
    # def fillrectangle

    '''
    def _fill(self):
        # type: () -> BaseScene
        return self \
            .fill(self._x, self._y, self._color)

    def _fillcircle(self, _r, _style):
        # todo
        return self \
            .fillcircle(self._x, self._y, _r, self._color, _style)

    def _fillrectangle(self, _w, _h):
        # todo
        return self \
            .fillrectangle(self._x, self._y, _w, _h, self._color)
    '''
