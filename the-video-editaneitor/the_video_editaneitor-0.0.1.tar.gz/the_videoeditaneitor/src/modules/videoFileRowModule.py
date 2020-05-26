import pygame as pg
import pygame_gui as pgu
import ntpath

from the_videoeditaneitor.src.modules.videoModule import was_exported

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


class VideoFileRow:

    def __init__(self, _path_video, _size, manager, container):
        self.path_video = _path_video
        self.container = container
        self.manager = manager
        self.is_draw = False
        self.text_box: pgu.elements.UITextBox = None
        self.load_button: pgu.elements.UIButton = None

        self.size = _size
        self.dest = (0, 0)

        self.btn_size = (30, self.size[1])
        self.lbl_size = (self.size[0] - self.btn_size[0], self.size[1])

    def draw(self, _relative_dest):
        if not self.is_draw:
            self.dest = _relative_dest

            load_button_dest = (self.dest[0] + self.lbl_size[0], self.dest[1])

            self.text_box = pgu.elements.UITextBox(
                html_text=path_leaf(self.path_video),
                relative_rect=pg.Rect(self.dest, self.lbl_size),
                manager=self.manager, container=self.container)

            self.load_button = pgu.elements.UIButton(
                relative_rect=pg.Rect(load_button_dest, self.btn_size),
                text='L',
                manager=self.manager, container=self.container)

            if was_exported(self.path_video):
                self.text_box.background_colour = pg.Color(*pg.color.THECOLORS["darkolivegreen"])
                self.text_box.rebuild()

            self.is_draw = True

    def make_selected(self):
        if was_exported(self.path_video):
            self.text_box.background_colour = pg.Color(*pg.color.THECOLORS["darkolivegreen4"])
            self.text_box.rebuild()
        else:
            self.text_box.background_colour = pg.Color(*pg.color.THECOLORS["gray40"])
            self.text_box.rebuild()

    def make_non_selected(self):
        if was_exported(self.path_video):
            self.text_box.background_colour = pg.Color(*pg.color.THECOLORS["darkolivegreen"])
            self.text_box.rebuild()
        else:
            self.text_box.background_colour = pg.Color(33, 40, 45, 255)
            self.text_box.rebuild()

    def kill(self):
        if self.is_draw:
            self.text_box.kill()
            self.load_button.kill()
            self.is_draw = False