import pygame as pg
import pygame_gui as pgu

from the_videoeditaneitor.src.modules.videoModule import VideoModule
from the_videoeditaneitor.src.modules.menuModule import MenuModule
from the_videoeditaneitor.src.modules.videoFilesModule import VideoFileModule


def start():
    window_size = (1000, 700)

    menu_panel_dest = (0, 0)
    menu_panel_size = (window_size[0], 50)

    files_panel_dest = (0, menu_panel_size[1])
    files_panel_size = (window_size[0] - 650, window_size[1] - menu_panel_size[1])

    video_panel_dest = (files_panel_size[0], menu_panel_size[1])
    video_panel_size = (window_size[0] - files_panel_size[0], window_size[1] - menu_panel_size[1])

    pg.init()
    pg.display.set_caption('The Video Editaneitor')
    window_surface = pg.display.set_mode(window_size)

    background = pg.Surface(window_size)
    background.fill(pg.Color('#000000'))

    manager = pgu.UIManager(window_size)

    video_module = VideoModule(manager, dest=video_panel_dest, size=video_panel_size)

    file_module = VideoFileModule(manager, video_module, dest=files_panel_dest, size=files_panel_size)

    menu_module = MenuModule(manager, file_module, video_module, dest=menu_panel_dest, size=menu_panel_size)

    file_module.set_files_path('D:\\livenessData\\videos_original\\Vm9VdmOpzcs\\original\\')

    clock = pg.time.Clock()

    running = True
    while running:
        time_delta = clock.tick(video_module.fps) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                running = False

            menu_module.process_events(event)
            manager.process_events(event)

        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pg.display.update()

        video_module.update()
        file_module.update()
        menu_module.update()
