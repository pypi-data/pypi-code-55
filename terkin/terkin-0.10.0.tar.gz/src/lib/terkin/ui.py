# -*- coding: utf-8 -*-
# (c) 2017-2019 Andreas Motl <andreas@terkin.org>
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3

# https://github.com/pfalcon/picotui/issues/35

from picotui.screen import Screen
from picotui.widgets import *
from picotui.defs import *

# Set the list of all available DropDown choices
choices = ["Green1", "Green2", "Green3", "Red1", "Red2", "Red3", "Yellow1", "Yellow2", "Yellow3"]
# Copy the list of DropDown choices to another list for modifications
fchoices = choices[:]


class TerkinUi:

    def __init__(self):
        self.screen = Screen()

    def start(self):
        self.screen.init_tty()
        self.screen.enable_mouse()
        self.screen.attr_color(C_WHITE, C_BLUE)
        self.screen.cls()
        self.screen.attr_reset()

    def stop(self):
        self.screen.goto(0, 50)
        self.screen.cursor(True)
        self.screen.disable_mouse()
        self.screen.deinit_tty()

        #self.screen.attr_color(C_WHITE, C_BLUE)
        self.screen.cls()
        #self.screen.attr_reset()
        print()

    def example_listbox(self):
        """
        From https://github.com/hiveeyes/picotui/blob/master/examples/example_filter_listbox.py
        """

        self.screen.goto(1, 1)
        self.screen.wr('Picotui example: Filter listbox')

        d = Dialog(1, 3, 20, 12)

        # DropDown and ListBox widgets
        d.add(1, 1, "Dropdown:")
        w_dropdown = WDropDown(10, ["All", "Red", "Green", "Yellow"])
        d.add(11, 1, w_dropdown)

        d.add(1, 3, "List:")
        w_listbox = WListBox(16, 4, ["%s" % i for i in fchoices])
        d.add(1, 4, w_listbox)

        # Filter the ListBox based on the DropDown selection
        def dropdown_changed(w):
            fchoices.clear()
            for i in range(0, len(choices)):
                if w.items[w.choice] == "All" or w.items[w.choice] in choices[i]:
                    fchoices.append(choices[i])

            w_listbox.top_line = 0
            w_listbox.cur_line = 0
            w_listbox.row = 0
            w_listbox.items = ["%s" % items for items in fchoices]
            w_listbox.set_lines(w_listbox.items)
        w_dropdown.on("changed", dropdown_changed)

        b = WButton(8, "OK")
        d.add(2, 10, b)
        b.finish_dialog = ACTION_OK

        b = WButton(8, "Cancel")
        d.add(12, 10, b)
        b.finish_dialog = ACTION_CANCEL

        res = d.loop()
        print('res:', res)

    def example_menu(self):
        """
        From https://github.com/hiveeyes/picotui/blob/master/example_menu.py
        """

        # This routine is called to redraw screen "in menu's background"
        def screen_redraw(s, allow_cursor=False):
            s.attr_color(C_WHITE, C_BLUE)
            s.cls()
            s.attr_reset()
            d.redraw()

        # We have two independent widgets on screen: dialog and main menu,
        # so can't call their individual loops, and instead should have
        # "main loop" to route events to currently active widget, and
        # switch the active one based on special events.
        def main_loop():
            while 1:
                key = m.get_input()

                if isinstance(key, list):
                    # Mouse click
                    x, y = key
                    if m.inside(x, y):
                        m.focus = True

                if m.focus:
                    # If menu is focused, it gets events. If menu is cancelled,
                    # it loses focus. Otherwise, if menu selection is made, we
                    # quit with with menu result.
                    res = m.handle_input(key)
                    if res == ACTION_CANCEL:
                        m.focus = False
                    elif res is not None and res is not True:
                        return res
                else:
                    # If menu isn't focused, it can be focused by pressing F9.
                    if key == KEY_F9:
                        m.focus = True
                        m.redraw()
                        continue
                    # Otherwise, dialog gets input
                    res = d.handle_input(key)
                    if res is not None and res is not True:
                        return res

        d = Dialog(10, 5, 40, 13)
        d.add(1, 1, WLabel("Label:"))
        d.add(1, 2, WListBox(16, 4, ["choice%d" % i for i in range(10)]))
        d.add(1, 7, WDropDown(10, ["Red", "Green", "Yellow"]))

        b = WButton(8, "OK")
        d.add(3, 10, b)
        b.finish_dialog = ACTION_OK

        b = WButton(8, "Cancel")
        d.add(20, 10, b)
        b.finish_dialog = ACTION_CANCEL

        screen_redraw(self.screen)
        self.screen.set_screen_redraw(screen_redraw)

        from picotui.menu import WMenuBar, WMenuBox
        menu_file = WMenuBox([("Open...", "Open"), ("Save", "S"), ("Save as...", "Sa"), ("Exit", "ex")])
        menu_edit = WMenuBox([("Copy", "copy"), ("Paste", "paste")])
        m = WMenuBar([("File", menu_file), ("Edit", menu_edit), ("About", "About")])
        m.permanent = True
        m.redraw()

        res = main_loop()
