"""
main application class for GUIApp-conform Kivy app
==================================================

This ae portion is providing two classes (:class:`FrameworkApp`
and :class:`KivyMainApp` and some useful constants.

The class :class:`KivyMainApp` is implementing a main app
class that is reducing the amount of code needed for
to create a Python application based on the
:ref:`kivy framework<kivy.org>`.

:class:`KivyMainApp` is based on the following classes:

* the abstract base class :class:`~ae.gui_app.MainAppBase`
  which adds the concepts of :ref:`application status`
  (including :ref:`app-state-variables` and :ref:`app-state-constants`),
  :ref:`application flow` and :ref:`application events`.
* the class :class:`~ae.console.ConsoleApp` is adding
  :ref:`config-files`, :ref:`config-variables`
  and :ref:`config-options`.
* the class :class:`~ae.core.AppBase` is adding
  :ref:`application logging` and :ref:`application debugging`.


The main app class :class:`KivyMainApp` is also encapsulating the
:class:`Kivy app class <kivy.app.App>` within the :class:`FrameworkApp`.
An instance of the Kivy app class can be directly accessed from
the main app class instance via the
:attr:`~KivyMainApp.framework_app` attribute.


unit tests
----------

For to run the unit tests of this ae portion you need a system
with a graphic system supporting at least V 2.0 of OpenGL and the
kivy framework installed.

.. note::
    unit tests does have 100 % coverage but are currently not passing the gitlab CI
    tests because we failing in setup a proper running window system on the
    python image that all ae portions are using.

Any help for to fix the problems with the used gitlab CI image is highly appreciated.

"""
import os
from typing import Any, Callable, Dict, Optional, Tuple, Type

# import jnius                                                                # type: ignore
import kivy                                                                 # type: ignore
from kivy.app import App                                                    # type: ignore
from kivy.core.window import Window                                         # type: ignore
from kivy.factory import Factory, FactoryException                          # type: ignore
from kivy.lang import Builder                                               # type: ignore
# pylint: disable=no-name-in-module
from kivy.properties import BooleanProperty, DictProperty, ListProperty     # type: ignore
from kivy.core.audio import SoundLoader                                     # type: ignore
from kivy.uix.widget import Widget                                          # type: ignore
from plyer import vibrator                                                  # type: ignore

from ae.files import FilesRegister, CachedFile                              # type: ignore
# id_of_flow not used here - added for easier import in app project
# noinspection PyUnresolvedReferences
from ae.gui_app import (                                                    # type: ignore
    THEME_LIGHT_BACKGROUND_COLOR, THEME_LIGHT_FONT_COLOR, THEME_DARK_BACKGROUND_COLOR, THEME_DARK_FONT_COLOR,
    MainAppBase
)                                                                           # type: ignore


__version__ = '0.0.21'


kivy.require('1.9.1')  # currently using 1.11.1 but at least 1.9.1 is needed for Window.softinput_mode 'below_target'

# if the entry field is on top of the screen then it will be disappear with below_target mode
# and in the default mode ('') the keyboard will cover the entry field if it is in the lower part of the screen
# therefore commented out the following two code lines (and setting it now depending on the entry field y position)
# if Window:                                  # is None on gitlab ci
#    Window.softinput_mode = 'below_target'  # ensure android keyboard is not covering Popup/text input if at bottom

MAIN_KV_FILE_NAME = 'main.kv'           #: default file name of the main kv file

LOVE_VIBRATE_PATTERN = (0.0, 0.12, 0.12, 0.21, 0.03, 0.12, 0.12, 0.12)
""" short/~1.2s vibrate pattern for fun/love notification. """

ERROR_VIBRATE_PATTERN = (0.0, 0.09, 0.09, 0.18, 0.18, 0.27, 0.18, 0.36, 0.27, 0.45)
""" long/~2s vibrate pattern for error notification. """

CRITICAL_VIBRATE_PATTERN = (0.00, 0.12, 0.12, 0.12, 0.12, 0.12,
                            0.12, 0.24, 0.12, 0.24, 0.12, 0.24,
                            0.12, 0.12, 0.12, 0.12, 0.12, 0.12)
""" very long/~2.4s vibrate pattern for critical error notification (sending SOS to the mobile world;) """


WIDGETS = '''\
#: import Window kivy.core.window.Window

#: import MIN_FONT_SIZE ae.gui_app.MIN_FONT_SIZE
#: import MAX_FONT_SIZE ae.gui_app.MAX_FONT_SIZE
#: import THEME_LIGHT_BACKGROUND_COLOR ae.gui_app.THEME_LIGHT_BACKGROUND_COLOR
#: import THEME_LIGHT_FONT_COLOR ae.gui_app.THEME_LIGHT_FONT_COLOR
#: import THEME_DARK_BACKGROUND_COLOR ae.gui_app.THEME_DARK_BACKGROUND_COLOR
#: import THEME_DARK_FONT_COLOR ae.gui_app.THEME_DARK_FONT_COLOR

#: import id_of_flow ae.gui_app.id_of_flow
#: import flow_key ae.gui_app.flow_key
#: import flow_key_split ae.gui_app.flow_key_split

<ThemeButton@ButtonBehavior+Label>:
    circle_fill_color: 0, 0, 0, 0
    square_fill_color: 0, 0, 0, 0
    fill_pos: self.fill_pos or self.pos
    fill_size: self.fill_size or self.size
    source: themeButtonImage.source
    size_hint: 0.003, None
    size_hint_min_x: self.height
    height: app.ae_states['font_size'] * 1.5
    font_size: app.ae_states['font_size']
    color: app.font_color
    canvas.before:
        Color:
            rgba: self.square_fill_color
        RoundedRectangle:
            pos: self.fill_pos or self.pos
            size: self.fill_size or self.size
        Color:
            rgba: self.circle_fill_color
        Ellipse:
            pos: self.fill_pos or self.pos
            size: self.fill_size or self.size
    Image:
        id: themeButtonImage
        source: root.source
        allow_stretch: True
        keep_ratio: False
        opacity: 1 if self.source else 0
        pos: self.parent.fill_pos or self.parent.pos
        size: self.parent.fill_size or self.parent.size


<ThemeInput@TextInput>:
    font_size: app.ae_states['font_size']
    cursor_color: app.font_color
    foreground_color: app.font_color
    background_color: Window.clearcolor

<FlowButton@ThemeButton>:
    ae_flow_id: ''
    ae_clicked_kwargs: dict(popup_kwargs=dict(parent=self))
    ae_icon_name: ""
    on_release: app.main_app.change_flow(self.ae_flow_id, **self.ae_clicked_kwargs)
    source:
        app.main_app.img_file(self.ae_icon_name or flow_key_split(self.ae_flow_id)[0], \
                              app.ae_states['font_size'], app.ae_states['light_theme'])


<OptionalButton@FlowButton>:
    visible: True
    size_hint: None, None
    width: self.width if self.visible else 0
    width: self.height if self.visible else 0
    disabled: not self.visible
    opacity: 1 if self.visible else 0


# DropDown flow gets handled identical like for a Popup
<FlowDropDown@DropDown>:
    ae_closed_kwargs: dict(flow_id=id_of_flow('', '')) if app.main_app.flow_path_action(-2) in ('', 'enter') else dict()
    on_dismiss: app.main_app.change_flow(id_of_flow('close', 'flow_popup'), **self.ae_closed_kwargs)
    auto_width: False
    width: min(Window.width - (self.attach_to.x if self.attach_to else sp(90)) - sp(9), sp(960))
    canvas.after:
        Color:
            rgba: app.font_color
        Line:
            width: sp(1.8)
            rounded_rectangle: self.x, self.y, self.width, self.height, sp(9)


<FlowPopup@Popup>:
    ae_closed_kwargs: dict(flow_id=id_of_flow('', '')) if app.main_app.flow_path_action(-2) in ('', 'enter') else dict()
    on_dismiss: app.main_app.change_flow(id_of_flow('close', 'flow_popup'), **self.ae_closed_kwargs)
    auto_dismiss: True
    separator_color: app.font_color
    title_align: 'center'
    title_size: app.main_app.font_size


<UserPreferencesButton@FlowButton>:
    ae_flow_id: id_of_flow('open', 'user_preferences')
    circle_fill_color: 0.69, 0.69, 0.99, 0.9

<UserPreferencesOpenPopup@FlowDropDown>:
    ChangeColorButton:
        color_name: 'flow_id_ink'
    ChangeColorButton:
        color_name: 'flow_path_ink'
    ChangeColorButton:
        color_name: 'selected_item_ink'
    ChangeColorButton:
        color_name: 'unselected_item_ink'
    FontSizeButton:
        # pass
    UserPrefSlider:
        app_state_name: 'sound_volume'
        cursor_image: 'atlas://data/images/defaulttheme/audio-volume-high'
    # UserPrefSlider:    current kivy module vibrator.py does not support amplitudes arg of android api
    #    app_state_name: 'vibrate_amplitude'
    #    cursor_image: app.main_app.img_file('vibrate', app.ae_states['font_size'], app.ae_states['light_theme'])
    BoxLayout:
        size_hint_y: None
        height: app.ae_states['font_size'] * 1.5
        ThemeButton:
            text: "dark"
            on_release: app.main_app.change_flow(id_of_flow('change', 'light_theme'), light_theme=False)
            color: THEME_DARK_FONT_COLOR or self.color
            square_fill_color: THEME_DARK_BACKGROUND_COLOR or self.square_fill_color
        ThemeButton:
            text: "light"
            on_release: app.main_app.change_flow(id_of_flow('change', 'light_theme'), light_theme=True)
            color: THEME_LIGHT_FONT_COLOR or self.color
            square_fill_color: THEME_LIGHT_BACKGROUND_COLOR or self.square_fill_color


<UserPrefSlider@Slider>:
    app_state_name: ''
    value: app.ae_states.get(self.app_state_name, 1.0)
    on_value: app.main_app.change_app_state(self.app_state_name, self.value)
    min: 0.0
    max: 1.0
    step: 0.03
    size_hint_y: None
    height: app.ae_states['font_size'] * 1.5
    cursor_size: app.ae_states['font_size'] * 1.5, app.ae_states['font_size'] * 1.5
    padding: app.ae_states['font_size'] * 2.4
    value_track: True
    value_track_color: app.font_color
    canvas.before:
        Color:
            rgba: Window.clearcolor
        RoundedRectangle:
            pos: self.pos
            size: self.size


<FontSizeButton@FlowButton>:
    ae_flow_id: id_of_flow('edit', 'font_size')
    ae_clicked_kwargs: dict(popup_kwargs=dict(parent_popup_to_close=self.parent.parent, parent=self))
    square_fill_color: Window.clearcolor

<FontSizeEditPopup@FlowDropDown>:
    parent_popup_to_close: None
    on_select:
        app.main_app.change_flow(id_of_flow('change', 'font_size'), \
        font_size=args[1], popups_to_close=(self.parent_popup_to_close, ))
    FontSizeSelectButton:
        font_size: MIN_FONT_SIZE
    FontSizeSelectButton:
        font_size: MIN_FONT_SIZE + (MAX_FONT_SIZE - MIN_FONT_SIZE) * 1 / 6
    FontSizeSelectButton:
        font_size: MIN_FONT_SIZE + (MAX_FONT_SIZE - MIN_FONT_SIZE) * 2 / 6
    FontSizeSelectButton:
        font_size: (MIN_FONT_SIZE + MAX_FONT_SIZE) / 2
    FontSizeSelectButton:
        font_size: MIN_FONT_SIZE + (MAX_FONT_SIZE - MIN_FONT_SIZE) * 4 / 6
    FontSizeSelectButton:
        font_size: MIN_FONT_SIZE + (MAX_FONT_SIZE - MIN_FONT_SIZE) * 5 / 6
    FontSizeSelectButton:
        font_size: MAX_FONT_SIZE

<FontSizeSelectButton@Button>:
    # text: f'Aa Bb Zz {round(self.font_size)}'      F-STRINGS don't work - displays always 15 as font size
    text: 'Aa Bb Zz {}'.format(round(self.font_size))
    on_release: self.parent.parent.select(self.font_size)
    size_hint_y: None
    size: self.texture_size
    color: app.font_color
    background_normal: ''
    background_color: Window.clearcolor


<ChangeColorButton@FlowButton>:
    color_name: 'flow_id_ink'
    ae_flow_id: id_of_flow('open', 'color_picker', self.color_name)
    ae_clicked_kwargs: dict(popup_kwargs=dict(parent=self))
    square_fill_color: Window.clearcolor
    circle_fill_color: app.ae_states[self.color_name]
    text: self.color_name

<ColorPickerOpenPopup@FlowDropDown>:
    ColorPicker:
        color: app.ae_states[root.attach_to.color_name] if root.attach_to else (0, 0, 0, 0)
        on_color: root.attach_to and app.main_app.change_app_state(root.attach_to.color_name, tuple(args[1]))
        size_hint_y: None
        height: self.width
        canvas.before:
            Color:
                rgba: Window.clearcolor
            RoundedRectangle:
                pos: self.pos
                size: self.size
'''
""" helper widgets with integrated app flow and observers ensuring change of app states (e.g. theme and size) """


class FrameworkApp(App):
    """ kivy framework app class proxy redirecting events and callbacks to the main app class instance. """

    landscape = BooleanProperty()                           #: True if app win width is bigger than the app win height
    font_color = ListProperty(THEME_DARK_FONT_COLOR)        #: rgba color of the font used for labels/buttons/...
    ae_states = DictProperty()                              #: duplicate of MainAppBase app state for events/binds

    def __init__(self, main_app: 'KivyMainApp', **kwargs):
        """ init kivy app """
        self.main_app = main_app                            #: set reference to KivyMainApp instance
        self.title = main_app.app_title                     #: set kivy.app.App.title
        self.icon = os.path.join("img", "app_icon.png")     #: set kivy.app.App.icon

        super().__init__(**kwargs)

        # redirecting class name, app name and directory to the main app class for kv/ini file names is
        # .. no longer needed because main.kv get set in :meth:`KivyMainApp.init_app` and app states
        # .. get stored in the :ref:`ae config files <config-files>`.
        # self.__class__.__name__ = main_app.__class__.__name__
        # self._app_name = main_app.app_name
        # self._app_directory = '.'

    def build(self) -> Widget:
        """ kivy build app callback """
        self.main_app.po('App.build(), user_data_dir', self.user_data_dir,
                         "config files", getattr(self.main_app, '_cfg_files'))

        Window.bind(on_resize=self.win_pos_size_change,
                    left=self.win_pos_size_change,
                    top=self.win_pos_size_change,
                    on_key_down=self.key_press_from_kivy,
                    on_key_up=self.key_release_from_kivy)

        return Factory.Main()

    def key_press_from_kivy(self, keyboard, key_code, _scan_code, key_text, modifiers) -> bool:
        """ convert and redistribute key down/press events coming from Window.on_key_down.

        :param keyboard:        used keyboard.
        :param key_code:        key code of pressed key.
        :param _scan_code:      key scan code of pressed key.
        :param key_text:        key text of pressed key.
        :param modifiers:       list of modifier keys (including e.g. 'capslock', 'numlock', ...)
        :return:                True if key event got processed used by the app, else False.
        """
        return self.main_app.key_press_from_framework(
            "".join(_.capitalize() for _ in sorted(modifiers) if _ in ('alt', 'ctrl', 'meta', 'shift')),
            keyboard.command_keys.get(key_code) or key_text or str(key_code))

    def key_release_from_kivy(self, keyboard, key_code, _scan_code) -> bool:
        """ key release/up event. """
        return self.main_app.call_method('on_key_release', keyboard.command_keys.get(key_code, str(key_code)))

    def on_start(self):
        """ kivy app start event.

        Fired after call of :meth:`MainAppBase.run_app` method and MainAppBase.on_app_start event.

        Kivy just created the main layout by calling its :meth:`~kivy.app.App.build` method and
        attached it to the main window.
        """
        self.main_app.framework_win = self.root.parent
        self.win_pos_size_change()  # init. app./self.landscape (on app startup and after build)
        self.main_app.call_method('on_kivy_app_start')

    def on_pause(self) -> bool:
        """ app pause event """
        self.main_app.save_app_states()
        self.main_app.call_method('on_app_pause')
        return True

    def on_resume(self) -> bool:
        """ app resume event """
        self.main_app.load_app_states()
        self.main_app.call_method('on_app_resume')
        return True

    def on_stop(self):
        """ quit app event (:meth:`MainAppBase.stop_app` emits the `on_app_stop` event) """
        self.main_app.save_app_states()
        self.main_app.call_method('on_kivy_app_stop')

    def win_pos_size_change(self, *_):
        """ resize handler updates :attr:`~MainAppBase.win_rectangle` app state and :attr:`~FrameworkApp.landscape`. """
        self.main_app.win_pos_size_change(Window.left, Window.top, Window.width, Window.height)


class KivyMainApp(MainAppBase):
    """ Kivy application """
    flow_id_ink: tuple = (0.99, 0.99, 0.69, 0.69)           #: rgba color tuple for flow id / drag&drop node placeholder
    flow_path_ink: tuple = (0.99, 0.99, 0.39, 0.48)         #: rgba color tuple for flow_path/drag&drop item placeholder
    selected_item_ink: tuple = (0.69, 1.0, 0.39, 0.18)      #: rgba color tuple for list items (selected)
    unselected_item_ink: tuple = (0.39, 0.39, 0.39, 0.18)   #: rgba color tuple for list items (unselected)

    # abstract methods

    def init_app(self, framework_app_class: Type[FrameworkApp] = FrameworkApp
                 ) -> Tuple[Optional[Callable], Optional[Callable]]:
        """ initialize framework app instance and prepare app startup.

        :param framework_app_class:     class to create app instance (optionally extended by app project).
        :return:                        callable for to start and stop/exit the GUI event loop.
        """
        Builder.load_string(WIDGETS)

        win_rect = self.win_rectangle
        if win_rect:
            Window.left, Window.top = win_rect[:2]
            Window.size = win_rect[2:]

        self.framework_app = framework_app_class(self)
        if os.path.exists(MAIN_KV_FILE_NAME):
            self.framework_app.kv_file = MAIN_KV_FILE_NAME
        self._update_observable_app_states(self.retrieve_app_states())  # copy app states to duplicate DictProperty

        self.change_light_theme(self.light_theme)

        return self.framework_app.run, self.framework_app.stop

    # overwritten and helper methods

    def change_light_theme(self, light_theme: bool):
        """

        :param light_theme:
        :return:
        """
        Window.clearcolor = THEME_LIGHT_BACKGROUND_COLOR if light_theme else THEME_DARK_BACKGROUND_COLOR
        self.framework_app.font_color = THEME_LIGHT_FONT_COLOR if light_theme else THEME_DARK_FONT_COLOR

    @staticmethod
    def class_by_name(class_name: str) -> Optional[Type]:
        """ resolve kv widgets """
        try:
            return Factory.get(class_name)
        except (FactoryException, AttributeError):
            return None

    def load_sounds(self):
        """ override for to pre-load audio sounds from app folder snd into sound file cache. """
        self.sound_files = FilesRegister('snd', file_class=CachedFile,
                                         object_loader=lambda f: SoundLoader.load(f.path))

    def on_flow_widget_focused(self):
        """ set focus to the widget referenced by the current flow id. """
        liw = self.widget_by_flow_id(self.flow_id)
        self.vpo(f"KivyMainApp.on_flow_widget_focused() '{self.flow_id}'"
                 f" {liw} has={getattr(liw, 'focus', 'unsupported') if liw else ''}")
        if liw and getattr(liw, 'is_focusable', False) and not liw.focus:
            liw.focus = True

    def on_light_theme_change(self, flow_id: str, event_kwargs: Dict[str, Any]) -> bool:
        """ font size app state change event handler.

        :param flow_id:        flow id.
        :param event_kwargs:    event kwargs with key `'light_theme'` containing True|False for light|dark theme.
        :return:                True for to confirm change of flow id.
        """
        light_theme: bool = event_kwargs['light_theme']
        self.change_light_theme(light_theme)
        return super().on_light_theme_change(flow_id, event_kwargs)     # save light_theme app state

    def play_beep(self):
        """ make a short beep sound. """
        self.play_sound('error')

    def play_sound(self, sound_name: str):
        """ play audio/sound file. """
        self.vpo(f"KivyMainApp.play_sound {sound_name}")
        file: Optional[CachedFile] = self.find_sound(sound_name)
        if file:
            try:
                sound_obj = file.loaded_object
                sound_obj.pitch = file.properties.get('pitch', 1.0)
                sound_obj.volume = (
                    file.properties.get('volume', 1.0) * self.framework_app.ae_states.get('sound_volume', 1.))
                sound_obj.play()
            except Exception as ex:
                self.po(f"KivyMainApp.play_sound exception {ex}")
        else:
            self.dpo(f"KivyMainApp.play_sound({sound_name}) not found")

    def play_vibrate(self, pattern: Tuple = (0.03, 0.3)):
        """ play vibrate pattern. """
        self.vpo(f"KivyMainApp.play_vibrate {pattern}")
        try:        # added because is crashing with current plyer version (master should work)
            vibrator.pattern(pattern)
        # except jnius.jnius.JavaException as ex:
        #    self.po(f"KivyMainApp.play_vibrate JavaException {ex}, update plyer to git/master")
        except Exception as ex:
            self.po(f"KivyMainApp.play_vibrate exception {ex}")

    @staticmethod
    def prevent_keyboard_covering(input_box_bottom: float):
        """ prevent that the virtual keyboard popping up on mobile platforms is covering the text input field.

        :param input_box_bottom:    y position of the bottom of the input field box.
        """
        keyboard_height = Window.keyboard_height or Window.height / 3  # 'or'-fallback because SDL2 reports 0 kbd height
        Window.softinput_mode = 'below_target' if input_box_bottom < keyboard_height else ''

    def show_popup(self, popup_class: Type[Widget], **popup_attributes) -> Widget:
        """ open Popup using the `open` method. Overwriting the main app class method.

        :param popup_class:         class of the Popup widget/window.
        :param popup_attributes:    args for to be set as attributes of the popup class instance plus an optional
                                    `'parent'` kwarg that will be passed as the popup parent widget arg
                                    to the popup.open method; if parent does not get passed then
                                    self.framework_win will passed into the popup.open method as the widget argument.
        :return:                    created and displayed/opened popup class instance.
        """
        self.dpo(f"KivyAppBase.show_popup {popup_class} {popup_attributes}")

        parent = popup_attributes.pop('parent', self.framework_win)
        popup_instance = popup_class()
        for attr, value in popup_attributes.items():
            setattr(popup_instance, attr, value)

        if not hasattr(popup_instance, 'close') and hasattr(popup_instance, 'dismiss'):
            popup_instance.close = popup_instance.dismiss   # create close() method alias for DropDown.dismiss() method

        self.prevent_keyboard_covering(popup_instance.y)
        popup_instance.open(parent)

        return popup_instance
