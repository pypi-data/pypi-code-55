import pygame as pg
import pygame_gui as pgu


class MenuModule:

    def __init__(self, _manager, file_module, video_module, dest=(0, 0), size=(800, 600)):
        self.manager = _manager
        self.file_module = file_module
        self.video_module = video_module
        self.dest = dest
        self.size = size
        self.menu_panel = pgu.elements.UIPanel(manager=_manager, starting_layer_height=0, relative_rect=pg.Rect(dest, size))

        self.btn_open_file_dest = (0, 0)
        self.btn_open_file_size = (100, size[1] - 5)

        self.btn_help_dest = (size[0] - 40, 0)
        self.btn_help_size = (40, size[1] - 5)

        self.wds_help_dest = (dest[0] + 50, dest[1] + 100)
        self.wds_help_size = (size[0] - 100, 500)

        self.wds_help = None

        self.lbl_file_opened_dest = (self.btn_open_file_size[0], 0)
        self.lbl_file_opened_size = (400, size[1] - 5)

        self.btn_open_file = pgu.elements.UIButton(
                relative_rect=pg.Rect(self.btn_open_file_dest, self.btn_open_file_size),
                text='Open',
                manager=self.manager, container=self.menu_panel)

        self.lbl_file_opened = pgu.elements.UITextBox(html_text="N/A", manager=self.manager,
                               container=self.menu_panel,
                               relative_rect=pg.Rect(self.lbl_file_opened_dest, self.lbl_file_opened_size))
        self.file_dialog = None

        self.btn_help = pgu.elements.UIButton(
            relative_rect=pg.Rect(self.btn_help_dest, self.btn_help_size),
            text='?',
            manager=self.manager, container=self.menu_panel)
        self.wds_help = None

    def process_events(self, event):
        # Keyboard events
        if event.type == pg.KEYDOWN:

            # Play
            if event.key == pg.K_p:
                self.video_module.play()

            # Pause
            if event.key == pg.K_SPACE:
                self.video_module.pause()

            # One frame backward
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                self.video_module.one_frame_backward()

            # One frame forward
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                self.video_module.one_frame_forward()

            # Set ini
            if event.key == pg.K_1:
                self.video_module.select_frame_ini()

            # Set end
            if event.key == pg.K_2:
                self.video_module.select_frame_end()

            # Export
            if event.key == pg.K_e:
                self.video_module.export()
                self.file_module.next_row()

            # Export And Next Non Exported
            if event.key == pg.K_s:
                self.video_module.export()
                self.file_module.next_row_not_exported()

            # load Next row video
            if event.key == pg.K_n:
                self.file_module.next_row()

            # load Next row video
            if event.key == pg.K_m:
                self.file_module.next_row_not_exported()

            # load Previous row video
            if event.key == pg.K_b:
                self.file_module.prev_row()

    def __get_help_text(self):
        return "<br>" \
                "[P]               -> Play Video <br>" \
                "[S]               -> Export <br>" \
                "[N]               -> Next Video <br>" \
                "[M]               -> Next Non Exported Video <br>" \
                "[B]               -> Previous Video <br>" \
                "[1]               -> Select Frame Ini <br>" \
                "[2]               -> Select Frame End <br>" \
                "[Space_bar]       -> Pause or Unpause <br>" \
                "[Arrow_left]      -> Frame Backward <br>" \
                "[Arrow_right]     -> Frame Forward <br>"\
                "[ESCAPE]          -> Quit <br>"


    def update(self):

        if self.btn_open_file.check_pressed():
            self.file_dialog = pgu.windows.UIFileDialog(
                rect=pg.Rect((0, 0), (600, 700)),
                manager=self.manager,
                allow_picking_directories=True)

        if self.btn_help.check_pressed():
            self.wds_help = pgu.elements.ui_window.UIWindow(
                rect=pg.Rect(self.wds_help_dest, self.wds_help_size),
                manager=self.manager,
                window_display_title="Help")

            pgu.elements.ui_text_box.UITextBox(
                html_text=self.__get_help_text(),
                relative_rect=pg.Rect((0, 0), (self.wds_help_size[0] - 32, self.wds_help_size[1] - 60)),
                manager=self.manager,
                container=self.wds_help)

        if self.file_dialog is not None and self.file_dialog.ok_button.check_pressed():
            selected_path = str(self.file_dialog.current_file_path)

            self.lbl_file_opened.kill()
            self.lbl_file_opened = pgu.elements.UITextBox(html_text=selected_path, manager=self.manager,
                                                          container=self.menu_panel,
                                                          relative_rect=pg.Rect(self.lbl_file_opened_dest,
                                                                                self.lbl_file_opened_size))

            self.file_module.set_files_path(selected_path)
            self.file_dialog = None




