import pygame as pg
import pygame_gui as pgu
import glob
import os

from the_videoeditaneitor.src.modules.videoFileRowModule import VideoFileRow
from the_videoeditaneitor.src.modules.videoModule import VideoModule, was_exported

class VideoFileModule:

    def __init__(self, _manager, video_module: VideoModule, dest=(0, 0), size=(800, 600), page_size=18):
        self.manager = _manager
        self.video_module = video_module
        self.dest = dest
        self.size = size

        self.row_size = (self.size[0] - 5, int(self.size[1] / page_size))

        self.page = 0
        self.last_page = 0
        self.page_size = page_size

        self.row_selected: VideoFileRow = None

        self.btn_page_back_dest = (30, size[1] - 35)
        self.btn_page_back_size = (100, 30)

        self.btn_page_next_dest = (self.btn_page_back_dest[0] + self.btn_page_back_size[0] + 30, size[1] - 35)
        self.btn_page_next_size = (100, 30)

        self.lbl_page_info_dest = (self.btn_page_next_dest[0] + self.btn_page_next_size[0] + 30, size[1] - 35)
        self.lbl_page_info_size = (50, 30)

        self.files_path = ""
        self.is_video_loaded = True
        self.is_page_loaded = True
        self.video_file_rows = []
        self.draw()

    def draw(self):
        self.files_panel = pgu.elements.UIPanel(
            manager=self.manager,
            starting_layer_height=0,
            relative_rect=pg.Rect(self.dest, self.size))

        self.btn_page_back = pgu.elements.UIButton(
                relative_rect=pg.Rect(self.btn_page_back_dest, self.btn_page_back_size),
                text='Back',
                manager=self.manager, container=self.files_panel)

        self.btn_page_next = pgu.elements.UIButton(
                relative_rect=pg.Rect(self.btn_page_next_dest, self.btn_page_next_size),
                text='Next',
                manager=self.manager, container=self.files_panel)

        self.lbl_page_info = self.lbl_page_info = pgu.elements.UILabel(
                text="{}/{}".format(0, 0),
                manager=self.manager,
                container=self.files_panel,
                relative_rect=pg.Rect(self.lbl_page_info_dest, self.lbl_page_info_size))

    def update(self):
        self.__load_file_path()
        self.__draw_page()

        if self.btn_page_next.check_pressed():
            if self.page + 1 < self.last_page:
                self.__set_page(self.page + 1)

        if self.btn_page_back.check_pressed():
            if self.page - 1 >= 0:
                self.__set_page(self.page - 1)

        self.__btn_selected_on_click()

    def set_files_path(self, _files_path):
        self.files_path = _files_path
        self.is_video_loaded = False

    def next_row(self):
        # calculate the next video
        next_video_row = None
        if self.video_file_rows is not None:
            if self.row_selected is None:
                next_video_row = self.video_file_rows[0]
            else:
                # calculate the next index in the array of rows
                next_row_index = self.video_file_rows.index(self.row_selected) + 1
                # if exist
                if next_row_index < len(self.video_file_rows):
                    next_video_row = self.video_file_rows[next_row_index]

        if next_video_row:
            # make video_module load that video
            self.__select_row_video(next_video_row)
            # calculate the page of the new element and if is necessary change it
            # if next_row_index

    def next_row_not_exported(self):
        # calculate the next video
        next_video_row = None
        if self.video_file_rows is not None:
            if self.row_selected is None:
                next_video_row = self.video_file_rows[0]
            else:
                counter = 1
                while not next_video_row:
                    # calculate the next index in the array of rows
                    next_row_index = self.video_file_rows.index(self.row_selected) + counter
                    # if exist
                    if next_row_index < len(self.video_file_rows):
                        # if the video wasn't exported
                        if not was_exported(self.video_file_rows[next_row_index].path_video):
                            next_video_row = self.video_file_rows[next_row_index]
                        counter += 1

        if next_video_row:
            # make video_module load that video
            self.__select_row_video(next_video_row)
            # calculate the page of the new element and if is necessary change it
            # if next_row_index

    def prev_row(self):
        # calculate the previous video
        prev_video_row = None
        if self.video_file_rows is not None:
            if self.row_selected is None:
                prev_video_row = self.video_file_rows[0]
            else:
                # calculate the next index in the array of rows
                next_row_index = self.video_file_rows.index(self.row_selected) - 1
                # if exist
                if next_row_index >= 0:
                    prev_video_row = self.video_file_rows[next_row_index]

        if prev_video_row:
            # make video_module load that video
            self.__select_row_video(prev_video_row)
            # calculate the page of the new element and if is necessary change it
            # if next_row_index

    def __load_file_path(self):
        if not self.is_video_loaded:
            self.video_file_rows = []

            result = [y for x in os.walk(self.files_path) for y in glob.glob(os.path.join(x[0], '*chunk.mp4'))]

            for file_path in result:
                self.video_file_rows.append(VideoFileRow(file_path, self.row_size, self.manager, self.files_panel))

            self.__set_page(0)
            self.last_page = int(len(self.video_file_rows) / self.page_size) + 1
            self.is_video_loaded = True

    def __draw_page(self):
        if not self.is_page_loaded:
            row_page_ini = self.page * self.page_size
            row_page_end = ((self.page + 1) * self.page_size) - 1

            for i, video_file_row in enumerate(self.video_file_rows):
                if row_page_ini <= i < row_page_end:
                    video_file_row.draw((0, self.row_size[1] * (i - row_page_ini)))
                    if video_file_row == self.row_selected:
                        video_file_row.make_selected()
                else:
                    video_file_row.kill()

            self.lbl_page_info.text = "{}/{}".format(self.page + 1, self.last_page)
            self.lbl_page_info.rebuild()

            self.is_page_loaded = True

    def __set_page(self, page=0):
        print("page = {}".format(page))
        self.page = page
        self.is_page_loaded = False

    def __btn_selected_on_click(self):
        for video_file_row in self.video_file_rows:
            if video_file_row.is_draw and video_file_row.load_button.check_pressed() and video_file_row != self.row_selected:
                self.__select_row_video(video_file_row)

    def __select_row_video(self, video_file_row):
        self.video_module.set_path_video(video_file_row.path_video)

        # Unselect the old row
        if self.row_selected is not None:
            self.row_selected.make_non_selected()

        # Select the new one
        video_file_row.make_selected()
        self.row_selected = video_file_row


