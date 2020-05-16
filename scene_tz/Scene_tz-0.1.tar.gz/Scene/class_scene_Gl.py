# Импортируем все необходимые библиотеки:
import math

import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Scene.base_scene import BaseScene

global GLUT_STROKE_ROMAN


class Scene(BaseScene):
    def i_center(self):
        # type: () -> Scene
        return self \
            .i_move_to(0, 0)

    window = 0

    def project_init(self):
        gluPerspective(45, float(self.width) / float(self.height), 0.1, 100.0)

    def gl_idle(self):
        glutPostRedisplay()

    def __init__(self, width, height):
        # Здесь начинается выполнение программы
        # Использовать двойную буферизацию и цвета в формате RGB (Красный, Зеленый, Синий)
        super().__init__(width, height, None)

        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        glutInitWindowPosition(0, 0)
        self.window = glutCreateWindow(b"")
        glutDisplayFunc(self.gl_draw)
        glutIdleFunc(self.gl_idle)
        glutReshapeFunc(self.gl_resize_scene)
        glutKeyboardFunc(self.gl_key_pressed)
        glutMouseFunc(self.gl_mouse_handle)
        glutMotionFunc(self.gl_mouse_motion)
        glutPassiveMotionFunc(self.gl_mouse_motion_passive)
        glutMouseWheelFunc(self.gl_mouse_wheel)

        glClearColor(0.3, 0.3, 0.3, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)

        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.project_init()
        glMatrixMode(GL_MODELVIEW)

        self.init()
        self.reset_fps()

    fps = 0
    last_fps = 0

    fps_timer = 500

    def reset_fps(self, *args):  # args[0] - command
        self.last_fps = self.fps
        if self.last_fps > 0:
            ms = self.fps_timer / self.last_fps
            glutSetWindowTitle('%.3f' % (1000 / ms) + ' %.3f' % ms)
        self.fps = 0
        glutTimerFunc(self.fps_timer, self.reset_fps, 0)  # 0 - command

    def gl_mouse_wheel(self, *args):
        print(args)
        pass

    def gl_mouse_handle(self, *args):
        left_button = GLUT_LEFT_BUTTON
        middle_button = GLUT_MIDDLE_BUTTON
        right_button = GLUT_RIGHT_BUTTON
        wheel_up = 3
        wheel_down = 4
        state_down = GLUT_DOWN
        state_up = GLUT_UP
        button, state, x, y = args

        callbacks = {
            state_down: {
                left_button: self.on_mouse_left_down,
                middle_button: self.on_mouse_middle_down,
                right_button: self.on_mouse_right_down,
                wheel_up: None,
                wheel_down: None,
            },
            state_up: {
                left_button: self.on_mouse_left_up,
                middle_button: self.on_mouse_middle_up,
                right_button: self.on_mouse_right_up,
                wheel_up: self.on_mouse_wheel_up,
                wheel_down: self.on_mouse_wheel_down,
            }
        }
        if state in [state_down, state_up]:
            if button in callbacks[state]:
                callback = callbacks[state][button]
                if callback is not None:
                    callback(x, y)
            else:
                print(args)
        else:
            print(args)

    debug = False

    def print(self, string):
        if self.debug:
            print(string)

    start_click = 0, 0

    args_list = []

    left_button_down = False
    middle_button_down = False
    right_button_down = False

    def on_mouse_left_down(self, x, y):
        self.print('callback on_mouse_left_down in point (%d, %d)' % (x, y))
        self.start_click = x, y
        self.left_button_down = True

    def on_mouse_left_up(self, x, y):
        self.print('callback on_mouse_left_up in point (%d, %d)' % (x, y))
        self.left_button_down = False
        lx, ly = self.start_click
        dx = 5
        length = math.sqrt(math.pow(lx - x, 2) + math.pow(ly - y, 2))
        if length < dx:
            self.on_mouse_click(x, y)

    def on_mouse_click(self, x, y):
        self.print('callback on_mouse_click in point (%d, %d)' % (x, y))

    def on_mouse_wheel_up(self, x, y):
        self.print('callback on_mouse_wheel_up in point (%d, %d)' % (x, y))
        glScaled(1.1, 1.1, 1.1)

    def on_mouse_wheel_down(self, x, y):
        self.print('callback on_mouse_wheel_down in point (%d, %d)' % (x, y))
        glScaled(0.9, 0.9, 0.9)

    def gl_mouse_motion_passive(self, x, y):
        self.print('callback gl_mouse_motion_passive in point (%d, %d)' % (x, y))
        return

    def gl_mouse_motion(self, x, y):
        self.print('callback gl_mouse_motion in point (%d, %d)' % (x, y))
        if not self.left_button_down:
            return

        mouse_dx = (y - self.start_click[1]) / 2
        mouse_dy = (x - self.start_click[0]) / 2

        self.start_click = x, y

        buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
        m = buffer.flatten()

        self.args_list.append([glRotatef, (mouse_dy, m[1], m[5], m[9])])
        self.args_list.append([glRotatef, (mouse_dx, m[0], m[4], m[8])])
        # glRotatef(mouse_dx, 1.0, 0.0, 0.0)
        # glRotatef(mouse_dy, 0.0, 1.0, 0.0)

    def on_mouse_right_up(self, x, y):
        self.print('callback on_mouse_right_up in point (%d, %d)' % (x, y))
        self.right_button_down = False

    def on_mouse_right_down(self, x, y):
        self.print('callback on_mouse_right_down in point (%d, %d)' % (x, y))
        self.right_button_down = True

    def on_mouse_middle_up(self, x, y):
        self.print('callback on_mouse_middle_up in point (%d, %d)' % (x, y))
        self.middle_button_down = False

    def on_mouse_middle_down(self, x, y):
        self.print('callback on_mouse_middle_down in point (%d, %d)' % (x, y))
        self.middle_button_down = True

    def gl_key_pressed(self, *args):
        print(args)
        if args[0] == b"\x1b":
            glutLeaveMainLoop()
            exit()

    def gl_resize_scene(self, width, height):
        if height == 0:
            height = 1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
        self.width = width
        self.height = height
        glMatrixMode(GL_MODELVIEW)

    def gl_draw(self):
        self.clear().redraw().some_cmd().show().fps += 1

    def some_cmd(self):
        # type: () -> Scene
        for args in self.args_list:
            funct = args.pop(0)
            params = args.pop(0)
            funct(*params)
        self.args_list.clear()

        return self

    def clear(self):
        # type: () -> Scene
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # glLoadIdentity()
        return self

    def show(self):
        # type: () -> Scene
        glutSwapBuffers()
        return self

    def draw(self):
        # type: () -> Scene
        # Запускаем основной цикл
        glutMainLoop()
        return self

    def redraw(self):
        # type: () -> Scene
        return self

    def init(self):
        return self

    # основные функции

    def lines(self):
        # type: () -> Scene
        """
        рисуем линии координат
        :return:
        """

        cx = self.width / 2  # центр по х
        cy = self.height / 2  # центр по у
        self \
            .c_set_color(0, 255, 0).i_move_to(0, -cy).i_line_step(0, self.height).i_move_to(-cx, 0).i_line_step(
            self.width, 0)
        return self

    def get_pixel(self, x, y):
        return 0

    def get_color(self, r, g, b):
        # type: (float, float, float) -> [float, float, float, float]
        return r / 255, g / 255, b / 255, 1

    def line(self, x1, y1, x2, y2, color):
        # type: (float, float, float, float, str) -> Scene
        glBegin(GL_LINES)
        glColor3d(*color)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()

        return self

    # обратная система координат

    def line_inv(self, x1, y1, x2, y2, color):
        # type: (float, float, float, float, [float, float, float]) -> Scene
        return self.line(x1, self.height - y1, x2, self.height - y2, color)

    def poly_lines(self, color, points):
        # type: (str, [float, float]) -> Scene
        first = points.pop(0)

        last = first

        for next_point in points:
            self.line(last[0], last[1], next_point[0], next_point[1], color)
            last = next_point

        if self.closed:
            self.line(last[0], last[1], first[0], first[1], color)

        return self

    def oval_spin(self, _cx, _cy, _r1, _r2, u, _color):
        # type: (float, float, float, float, float, [float, float, float]) -> Scene
        return self.arc(_cx, _cy, _r1, _r2, _color, 0, 360, u)

    def circle(self, _cx, _cy, _r, _color, poly_lines=False):
        # type: (float, float, float, str, bool) -> Scene

        if poly_lines:
            return self.arc(_cx, _cy, _r, _r, _color, 0, 360)

        # circle = self._img.circle(center=(_cx, _cy), r=_r, stroke=_color, stroke_width=1, fill="none")
        # self._img.add(circle)

        self.arc(_cx, _cy, _r, _r, _color, 0, 360)

        return self

    def set_pixel(self, _x, _y, _color):
        # type: (float, float, str) -> Scene
        glBegin(GL_POINTS)
        glColor3d(*_color)
        glVertex2f(_x, _y)
        glEnd()

        return self

    def setpixels(self, points, _color):
        # type: ([], str) -> Scene
        glBegin(GL_POINTS)
        glColor3d(*_color)
        for pt in points:
            glVertex2f(pt[0], pt[1])
        glEnd()

        return self


class SceneThird(Scene):
    def i_draw_text(self, *args):
        return self.draw_text(self._x, -self._y, *args)

    # todo move up
    def draw_text(self, x, y, *args):
        w = 6

        koef = 7  # self.width / w / 1000
        c_x, c_y = x * koef, y * koef
        glPushMatrix()
        c = 1 / 10000
        glScalef(c * w, c * w, c * w)
        width = 0
        height = glutStrokeHeight(GLUT_STROKE_ROMAN)

        params = list(args)
        fmt = params.pop(0)
        string = fmt % tuple(params)
        for p in string:
            width += glutStrokeWidth(GLUT_STROKE_ROMAN, ord(p))

        center = False
        if center:
            c_x -= width / 2
            c_y -= height / 4

        glTranslatef(c_x, c_y, 0)
        for p in string:
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(p))

        glPopMatrix()

    xRot = 0.0
    yRot = 0.0
    zRot = 0.0
    xTra = 0.0
    yTra = 0.0
    zTra = 0.0
    nSca = 1.0

    is_projection_ortho = True

    def lines(self):
        # type: () -> Scene
        """
        рисуем линии координат
        :return:
        """

        cx = self.width / 2  # центр по х
        cy = self.height / 2  # центр по у
        self \
            .c_set_color(0, 128, 128) \
            .i_move_to(0, -cy).i_line_step(0, self.height).i_move_to(-cx, 0).i_line_step(self.width, 0)
        return self

    def line(self, x1, y1, x2, y2, color):
        # type: (float, float, float, float, str) -> Scene
        glBegin(GL_LINES)
        glColor3d(*color)
        c_x, c_y = self.get_xy_scene(x1 + self.width / 2, y1 + self.height / 2)
        glVertex2f(c_x, c_y)
        c_x, c_y = self.get_xy_scene(x2 + self.width / 2, y2 + self.height / 2)
        glVertex2f(c_x, c_y)
        glEnd()

        return self

    def set_pixel(self, _x, _y, _color):
        # type: (float, float, str) -> Scene
        glBegin(GL_POINTS)
        glColor3d(*_color)
        c_x, c_y = self.get_xy_scene(_x + self.width / 2, _y + self.height / 2)
        glVertex2f(c_x, c_y)
        glEnd()

        return self

    def setpixels(self, points, _color):
        # type: ([], str) -> Scene
        glBegin(GL_POINTS)
        glColor3d(*_color)
        for pt in points:
            c_x, c_y = self.get_xy_scene(pt[0] + self.width / 2, pt[1] + self.height / 2)
            glVertex2f(c_x, c_y)
        glEnd()

        return self

    # получаем гльным координаты по координатам растровой сцены
    def get_xy_scene(self, x, y):
        c_x = (((x + 1) / self.width) * 2 - 1) * self.width / self.height - self.xTra * self.nSca
        c_y = 1 - ((y + 1) / self.height) * 2 - self.zTra * self.nSca
        return c_x, c_y

    # получаем координаты растровой сцены по гльным координатам
    def get_scene_xy(self, c_x, c_y):
        x = (self.height * (self.xTra * self.nSca + c_x) / self.width + 1) / 2 * self.width - 1
        y = - (self.height * ((self.zTra * self.nSca + c_y - 1) / 2) + 1)
        return x, y

    def project_init(self):
        if self.is_projection_ortho:
            ratio = self.height / self.width

            if self.width >= self.height:
                glOrtho(-1.0 / ratio, 1.0 / ratio, -1.0, 1.0, -10.0, 1.0)
            else:
                glOrtho(-1.0, 1.0, -1.0 * ratio, 1.0 * ratio, -10.0, 1.0)
        else:
            gluPerspective(90, float(self.width) / float(self.height), 1, 100.0)

    def resize_scene(self, dw, dh):
        pass

    def gl_resize_scene(self, width, height):
        if height == 0:
            height = 1

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if self.is_projection_ortho:
            ratio = height / width

            if width >= height:
                glOrtho(-1.0 / ratio, 1.0 / ratio, -1.0, 1.0, -10.0, 1.0)
            else:
                glOrtho(-1.0, 1.0, -1.0 * ratio, 1.0 * ratio, -10.0, 1.0)
        else:
            gluPerspective(60, float(width) / float(height), 1, 100.0)

        glViewport(0, 0, width, height)
        tmp = width / self.width, height / self.height
        self.width = width
        self.height = height
        self.resize_scene(*tmp)
        glMatrixMode(GL_MODELVIEW)

    def scale_plus(self):
        self.nSca = self.nSca * 1.1

    def scale_minus(self):
        self.nSca = self.nSca / 1.1

    def rotate_up(self):
        self.xRot += 1.0

    def rotate_down(self):
        self.xRot -= 1.0

    def rotate_left(self):
        self.zRot += 1.0

    def rotate_right(self):
        self.zRot -= 1.0

    def translate_down(self):
        self.zTra -= 0.05

    def translate_up(self):
        self.zTra += 0.05

    def default_scene(self):
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.zTra = 0
        self.nSca = 1

    def gl_key_pressed(self, *args):
        self.print(args)
        pass

    def clear(self):
        # type: () -> Scene
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glScalef(self.nSca, self.nSca, self.nSca)
        glTranslatef(0, self.zTra, 0.0)
        glRotatef(self.xRot, 1.0, 0.0, 0.0)
        glRotatef(self.yRot, 0.0, 1.0, 0.0)
        glRotatef(self.zRot, 0.0, 0.0, 1.0)

        return self

    def on_mouse_wheel_up(self, x, y):
        self.print('callback on_mouse_wheel_up in point (%d, %d)' % (x, y))
        self.scale_plus()

    def on_mouse_wheel_down(self, x, y):
        self.print('callback on_mouse_wheel_down in point (%d, %d)' % (x, y))
        self.scale_minus()


class Scene2d(SceneThird):
    """
    сцена для 2х мерных рисунков без вращения
    но с приближением и перемещением мышкой
    """
    ddx = 0
    ddy = 0

    last_ddx_ddy = 0, 0

    def clear(self):
        super().clear()
        glTranslatef(self.ddx, self.ddy, 0.0)
        return self

    right_click = 0, 0

    def on_mouse_right_down(self, x, y):
        super().on_mouse_right_down(x, y)
        self.right_click = x, y
        self.last_ddx_ddy = self.ddx, self.ddy
        glutSetCursor(GLUT_CURSOR_INFO)

    def on_mouse_right_up(self, x, y):
        super().on_mouse_right_up(x, y)
        glutSetCursor(GLUT_CURSOR_RIGHT_ARROW)

    def gl_mouse_motion(self, x, y):
        self.print('callback gl_mouse_motion in point (%d, %d)' % (x, y))

        if self.right_button_down:
            dx, dy = self.get_xy_scene(x - self.right_click[0] + self.width / 2,
                                       -y + self.right_click[1] + self.height / 2)
            # защита от дребезга руки
            if math.sqrt(math.pow(dx, 2) + math.pow(dy, 2)) > 0.05:
                self.ddx = self.last_ddx_ddy[0] + dx / self.nSca
                self.ddy = self.last_ddx_ddy[1] - dy / self.nSca

    def gl_key_pressed(self, *args):
        super().gl_key_pressed(*args)
        if args[0] == b"\x1b":
            glutLeaveMainLoop()
            exit()


class SceneSecond(Scene):
    left_button_down = False

    def on_mouse_left_down(self, x, y):
        self.start_click = x, y
        self.left_button_down = True

    def on_mouse_left_up(self, x, y):
        self.left_button_down = False

    def on_mouse_wheel_up(self, x, y):
        self.print('callback on_mouse_wheel_up in point (%d, %d)' % (x, y))
        glScaled(1.1, 1.1, 1.1)

    def on_mouse_wheel_down(self, x, y):
        self.print('callback on_mouse_wheel_down in point (%d, %d)' % (x, y))
        glScaled(0.9, 0.9, 0.9)

    def gl_mouse_motion(self, x, y):
        if not self.left_button_down:
            return
        '''
        mouse_dx = (x - self.start_click[0]) / 2
        mouse_dy = (y - self.start_click[1]) / 2

        self.start_click = x, y

        glRotatef(mouse_dx, 1.0, 0.0, 0.0)
        glRotatef(mouse_dy, 0.0, 1.0, 0.0)
        return
        '''
        look_speed = .2

        mouse_dx = (x - self.start_click[0]) / 20
        mouse_dy = (y - self.start_click[1]) / 20

        self.start_click = x, y

        buffer = glGetDoublev(GL_MODELVIEW_MATRIX)
        c = (-1 * numpy.mat(buffer[:3, :3]) * numpy.mat(buffer[3, :3]).T).reshape(3, 1)
        # c is camera center in absolute coordinates,
        # we need to move it back to (0,0,0)
        # before rotating the camera
        self.args_list.append([glTranslate, (c[0], c[1], c[2])])
        # glTranslate(c[0], c[1], c[2])
        m = buffer.flatten()
        self.args_list.append([glRotate, (mouse_dx * look_speed, m[1], m[5], m[9])])
        self.args_list.append([glRotate, (mouse_dy * look_speed, m[0], m[4], m[8])])
        # glRotate(mouse_dx * look_speed, m[1], m[5], m[9])
        # glRotate(mouse_dy * look_speed, m[0], m[4], m[8])

        # compensate roll
        # self.args_list.append([glRotated, (-math.atan2(-m[4], m[5]) * 57.295779513082320876798154814105, m[2], m[6], m[10])])
        # glRotated(-math.atan2(-m[4], m[5]) * 57.295779513082320876798154814105, m[2], m[6], m[10])
        self.args_list.append([glTranslate, (-c[0], -c[1], -c[2])])
        # glTranslate(-c[0], -c[1], -c[2])
