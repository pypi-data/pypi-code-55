from tkinter import *


class HPassGui:
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    def set_init_window(self):
        self.init_window_name.title("Hello Password")


def gui_start():
    init_window = Tk()
    h_pass_gui = HPassGui(init_window)
    h_pass_gui.set_init_window()
    init_window.mainloop()
