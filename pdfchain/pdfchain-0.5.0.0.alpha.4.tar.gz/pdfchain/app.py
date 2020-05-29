# Copyright (C) Martin Singer <martin.singer@web.de>
#
# This file is part of PDF Chain.
#
# PDF Chain is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PDF Chain is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PDF Chain.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Martin Singer

"""
@brief The Application Module.
@details
    The application manages the various windows and dialogs.
    It contains the preferences and about dialog
    as well as multiple application window instances.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib
from gi.repository import Gio
from gi.repository import Gtk

import pdfchain.paths as paths
import pdfchain.window as window
from pdfchain.preferences import Preferences


class Application(Gtk.Application):
    """
    """

    _preferences = None


    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="net.sourceforge.pdfchain",
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE, **kwargs)

        # Init preferences
        self._preferences = Preferences()

        # Add command line options
        self.add_main_option("test", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Command line test", None)


    # Overridden Class Signal Handler
    def do_startup(self):
        '''
        @brief Overwrite Virtual Class: Do Startup
        @details
            Connect the application menu actions with the application.
        @see <https://wiki.gnome.org/HowDoI/ApplicationMenu>
        '''
        Gtk.Application.do_startup(self)

        # Create and connect app menu entries
        action = Gio.SimpleAction.new("new", None)
        action.connect("activate", self.on_menu_new)
        self.add_action(action)

        action = Gio.SimpleAction.new("preferences", None)
        action.connect("activate", self.on_menu_preferences)
        self.add_action(action)

        # action = Gio.SimpleAction.new("shortcuts", None)
        # action.connect("activate", self.on_menu_shortcuts)
        # self.add_action(action)

        # action = Gio.SimpleAction.new("help", None)
        # action.connect("activate", self.on_menu_help)
        # self.add_action(action)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_menu_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("close", None)
        action.connect("activate", self.on_menu_close)
        self.add_action(action)

       # # Create app menu (deprecated)
       # builder_menu = Gtk.Builder()
       # builder_menu.add_from_file(paths.get_ui_file("menus.ui"))
       # self.set_app_menu(builder_menu.get_object("app-menu"))


    def do_activate(self):
        '''
        @brief Override Virtual Gio.Application Method.
        @details
            Appends the first application window.
        '''
        self._append_app_window()


    def do_command_line(self, command_line):
        '''
        TODO
        '''
        options = command_line.get_options_dict()
        options = options.end().unpack()

        if "test" in options:
            print("Test argument received: '%s'" % options["test"])

        self.activate()
        return 0


    # Menu Signal Handler
    def on_menu_new(self, action, param):
        '''
        @brief Application Menu Signal Handler: New Window
        @details
            Creates a new application window instance.
        @see window.AppWindowHandler.on_menu_app_new_activate()
        '''
        self._append_app_window()


    def on_menu_preferences(self, action, param):
        '''
        @brief Application Menu Signal Handler: Preferences
        @details
            Shows the preferences dialog.
        @see window.AppWindowHandler.on_menu_app_pref_activate()
        '''
        # self._preferences.set_transient_for(self.get_active_window())
        # self._preferences.run_dialog()
        self._preferences.run_dialog(self.get_active_window())


    def on_menu_shortcuts(self, action, param):
        '''
        @brief Application Menu Signal Handler: Shortcuts
        @details
            Shows the shortcuts information table dialog.
        @see window.AppWindowHandler.on_menu_app_scuts_activate()
        '''
        print("on_menu_shortcuts()") #TEST


    def on_menu_help(self, action, param):
        '''
        @brief Application Menu Signal Handler: Help
        @details
            Shows the helping manual.
        @see window.AppWindowHandler.on_menu_app_help_activate()
        '''
        print("on_menu_help()") #TEST


    def on_menu_about(self, action, param):
        '''
        @brief Application Menu Signal Handler: About PDF Chain NEO
        @details
            Shows the about dialog.
        @see window.AppWindowHandler.on_menu_app_about_activate()
        '''
        builder = Gtk.Builder()
        builder.add_from_file(paths.get_ui_file("dialogs.ui"))
        about_dialog = builder.get_object("dialog_about")
        about_dialog.set_transient_for(self.get_active_window())
        about_dialog.run()
        about_dialog.destroy()


    def on_menu_close(self, action, param):
        '''
        @brief Application Menu Signal Handler: Close Application
        @details
            Quits the application with all windows.
        @see window.AppWindowHandler.on_menu_app_close_activate()
        '''
        self.quit()


    # Methods
    def _append_app_window(self):
        '''
        Create a new ApplicaitonWindowHandler instance,
        which crates a new ApplicationWindow using the Builder from the UI file.
        It is not possible to create a second ApplicationWindow instance
        from the same Builder instance.
        A `copy.deepcopy` of the Builder object does not work.
        ("TypeError: GObject descendants' instances are non-copyable").
        If no independent builder object is used,
        all ApplicationWindow objects would point to the same Gtk widget
        in the background and no new instance will be shown.
        '''
        window.AppWindowHandler(self)
