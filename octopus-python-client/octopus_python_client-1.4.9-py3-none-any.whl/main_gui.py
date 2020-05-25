import logging

import PySimpleGUI as PySG
from urllib3.connectionpool import xrange

from octopus_python_client.actions import Actions
from octopus_python_client.common import Common, item_type_spaces, id_key, name_key
from octopus_python_client.config import Config


class MainGUI:
    DEFAULT_FONT_SIZE = 14
    DEFAULT_FONT = "Calibri"

    API_KEY = "api_key"
    ENDPOINT = "endpoint"
    OCTOPUS_NAME = "octopus_name"
    PASSWORD = "password"
    USER_NAME = "user_name"
    WORK_PATH = "work_path"

    EXIT = "Exit"
    LOGGER = logging.getLogger("MainGUI")
    NEXT = "Next >"
    PREV = "< Prev"
    SERVER_API_KEY_TEXT = 'API-KEY (must start with API-)'
    SERVER_ENDPOINT_TEXT = 'Server endpoint (must end with /api/)'
    SERVER_FOLDER_NAME_TEXT = 'Folder to store local data files (must be unique for each Octopus server)'
    SERVER_TOOL_TIP = ''
    SERVER_USER_PASSWORD_TEXT = 'user_name and password (will not be used if API-KEY exists); user_name'
    SOURCE_SERVER_JSON = "source_server.json"
    SOURCE_API_KEY = "source_api_key"
    SOURCE_ENDPOINT = "source_endpoint"
    SOURCE_LOCAL_DATA = "source_local_data"
    SOURCE_OCTOPUS_NAME = "source_octopus_name"
    SOURCE_PASSWORD = "source_password"
    SOURCE_USER_NAME = "source_user_name"
    SOURCE_WORK_PATH = "source_work_path"
    TITLE = "Octopus Python Client - Author: Tony Li & Cloud Engineering Team @ Tableau Software"
    WORK_PATH_TEXT = "The local path to store Octopus data for multiple servers"

    def __init__(self):
        self._config = Config()
        self._common = Common(config=self._config)
        self._source_server = Config(configuration_file_name=MainGUI.SOURCE_SERVER_JSON, is_source_server=True)
        self._source_common = Common(config=self._source_server)
        self._source_spaces = {}
        self._spaces = {}
        self._set_gui()

    def _process_action(self, actions_dict: dict):
        if not actions_dict:
            MainGUI.LOGGER.warning("empty select values")
            return
        for action, enabled in actions_dict.items():
            if enabled:
                self._config.action = action
                break
        self._config.save_config()

    def _process_server(self, server_dict: dict):
        if not server_dict:
            MainGUI.LOGGER.warning("empty server values")
            return
        self._config.__dict__.update((k, server_dict[k]) for k in self._config.__dict__.keys() & server_dict.keys())
        self._config.save_config()
        if MainGUI.SOURCE_ENDPOINT in server_dict:
            self._source_server.endpoint = server_dict.get(MainGUI.SOURCE_ENDPOINT)
            self._source_server.api_key = server_dict.get(MainGUI.SOURCE_API_KEY)
            self._source_server.user_name = server_dict.get(MainGUI.SOURCE_USER_NAME)
            self._source_server.password = server_dict.get(MainGUI.SOURCE_PASSWORD)
            self._source_server.octopus_name = server_dict.get(MainGUI.SOURCE_OCTOPUS_NAME)
            self._source_server.local_data = server_dict.get(MainGUI.SOURCE_LOCAL_DATA)
            self._source_server.work_path = server_dict.get(MainGUI.SOURCE_WORK_PATH)
            self._source_server.save_config()

    @staticmethod
    def _set_window(layout: list):
        return PySG.Window(MainGUI.TITLE, layout, auto_size_buttons=True, auto_size_text=True, resizable=True,
                           font=(MainGUI.DEFAULT_FONT, MainGUI.DEFAULT_FONT_SIZE))

    def _set_action_layout(self):
        return [[PySG.Text('Action selection')],
                # [PySG.Text('Enter something on Row 2'), PySG.InputText()],
                [PySG.Frame(layout=[
                    # [PySG.Checkbox('Checkbox', size=(10, 1)), PySG.Checkbox('My second checkbox!', default=True)],
                    # [PySG.Radio('My first Radio!     ', "RADIO1", default=True),
                    #  PySG.Radio('My second Radio!', "RADIO1")],
                    [PySG.Radio(f"{action} ({description})", 1, key=action,
                                default=True if self._config.action == action else False)]
                    for action, description in Actions.ACTIONS_DICT.items()], title='What do you want to do?',
                    key="select_action", tooltip='Select one action')],
                [PySG.Button(MainGUI.NEXT), PySG.Button(MainGUI.EXIT)]]
        # ,[PySG.Submit(), PySG.Cancel(), PySG.SimpleButton('Customized', button_color=('white', 'green'))]

    @staticmethod
    def _build_single_server_layout(endpoint, api_key, user_name, password, work_path, octopus_name,
                                    endpoint_key, api_key_key, user_name_key, password_key, work_path_key,
                                    octopus_name_key, frame_key, title_text="", tooltip=""):
        return [
            PySG.Frame(layout=[
                [PySG.Text(MainGUI.SERVER_ENDPOINT_TEXT),
                 PySG.InputText(key=endpoint_key, default_text=endpoint if endpoint else "")],
                [PySG.Text(MainGUI.SERVER_API_KEY_TEXT),
                 PySG.InputText(key=api_key_key, password_char="*", default_text=api_key if api_key else "")],
                [PySG.Text(MainGUI.SERVER_USER_PASSWORD_TEXT),
                 PySG.InputText(key=user_name_key, size=(10, None), default_text=user_name if user_name else ""),
                 PySG.Text(' password '),
                 PySG.InputText(key=password_key, size=(10, None), password_char="*",
                                default_text=password if password else "")],
                [PySG.Text(MainGUI.WORK_PATH_TEXT),
                 PySG.InputText(key=work_path_key, default_text=work_path if work_path else "")],
                [PySG.Text(MainGUI.SERVER_FOLDER_NAME_TEXT),
                 PySG.InputText(key=octopus_name_key, default_text=octopus_name if octopus_name else "")]
            ], title=title_text, tooltip=tooltip, key=frame_key)
        ]

    def _set_servers_layout(self):
        layout = []
        if self._config.action in Actions.MIGRATION_LIST:
            layout += [
                MainGUI._build_single_server_layout(
                    endpoint=self._source_server.endpoint, api_key=self._source_server.api_key,
                    user_name=self._source_server.user_name, password=self._source_server.password,
                    work_path=self._source_server.work_path, octopus_name=self._source_server.octopus_name,
                    endpoint_key=MainGUI.SOURCE_ENDPOINT, api_key_key=MainGUI.SOURCE_API_KEY,
                    user_name_key=MainGUI.SOURCE_USER_NAME, password_key=MainGUI.SOURCE_PASSWORD,
                    work_path_key=MainGUI.SOURCE_WORK_PATH, octopus_name_key=MainGUI.SOURCE_OCTOPUS_NAME,
                    title_text="The source Octopus server information", frame_key="source_server"),
                [PySG.Checkbox('The source server data is loaded from local files, not directly from server',
                               key=MainGUI.SOURCE_LOCAL_DATA, default=self._source_server.local_data)],
                [PySG.Text(f'\u21D3     \u21D3     \u21D3     \u21D3     \u21D3      {self._config.action}     '
                           f'\u21D3     \u21D3     \u21D3     \u21D3     \u21D3     ', justification='center',
                           font=(MainGUI.DEFAULT_FONT, MainGUI.DEFAULT_FONT_SIZE + 6))]
            ]
        layout += [
            [PySG.Text(f'Octopus servers and credentials for {self._config.action} '
                       f'({Actions.ACTIONS_DICT.get(self._config.action)})')],
            MainGUI._build_single_server_layout(
                endpoint=self._config.endpoint, api_key=self._config.api_key, user_name=self._config.user_name,
                password=self._config.password, work_path=self._config.work_path,
                octopus_name=self._config.octopus_name, endpoint_key=MainGUI.ENDPOINT, api_key_key=MainGUI.API_KEY,
                user_name_key=MainGUI.USER_NAME, password_key=MainGUI.PASSWORD, work_path_key=MainGUI.WORK_PATH,
                octopus_name_key=MainGUI.OCTOPUS_NAME, title_text="The Octopus server information",
                frame_key="octopus_server")
        ]
        return layout + [[PySG.Button(MainGUI.PREV), PySG.Button(MainGUI.NEXT), PySG.Button(MainGUI.EXIT)]]

    @staticmethod
    def _convert_spaces(list_spaces: list):
        space_dict = {}
        for space in list_spaces:
            space_dict[space.get(id_key)] = space.get(name_key)
        return space_dict

    @staticmethod
    def _get_single_server_spaces(common: Common):
        default_space_id = common.config.space_id
        common.config.space_id = None
        all_spaces = common.get_one_type_ignore_error(item_type=item_type_spaces)
        common.config.space_id = default_space_id
        list_spaces = common.get_list_items_from_all_items(all_items=all_spaces)
        if not list_spaces:
            PySG.popup_error(
                f"the {'source ' if common.config.is_source_server else ''}Octopus server does not have any spaces or "
                f"you do not have permission. Please make sure you have the correct server credentials",
                font=(MainGUI.DEFAULT_FONT, MainGUI.DEFAULT_FONT_SIZE))
            return {}
        spaces = MainGUI._convert_spaces(list_spaces=list_spaces)
        return spaces

    def _get_spaces(self):
        self._spaces = MainGUI._get_single_server_spaces(common=self._common)
        if self._config.action in Actions.MIGRATION_LIST:
            if self._source_server.local_data:
                # TODO read the local files and popup error for no spaces
                pass
            else:
                self._source_spaces = MainGUI._get_single_server_spaces(common=self._source_common)

    def _clear_spaces(self):
        self._spaces = {}
        self._source_spaces = {}

    @staticmethod
    def _to_matrix(lst, n):
        return [lst[i:i + n] for i in xrange(0, len(lst), n)]

    @staticmethod
    def _build_radios_matrix_layout(default_key: str, items_dict: dict, frame_key: str = "spaces", key_prefix: str = "",
                                    title: str = "", tooltip=""):
        radios = []
        for key in sorted(items_dict):
            value = items_dict.get(key)
            radios.append(PySG.Radio(f"{key} {value}", 1, key=f"{key_prefix}{key}",
                                     default=True if default_key == key else False))

        frames = []
        for row in MainGUI._to_matrix(radios, 4):
            frames.append([PySG.Frame(layout=[
                row
            ], title=title, key=frame_key, tooltip=tooltip, relief=PySG.RELIEF_FLAT)])

        return frames

    @staticmethod
    def _build_radios_layout(default_key: str, items_dict: dict, frame_key: str = "spaces", key_prefix: str = "",
                             title: str = "", tooltip=""):
        keys_list = list(items_dict.keys())
        keys_list.sort(key=lambda space_id: int(space_id.split("-")[1]))
        radios = []
        for key in keys_list:
            value = items_dict.get(key)
            radios.append(PySG.Radio(f"{key} {value}", 1, key=f"{key_prefix}{key}",
                                     default=True if default_key == key else False))

        return [PySG.Frame(layout=[
            [PySG.Radio(f"{key} {items_dict.get(key)}", 1, key=f"{key_prefix}{key}",
                        default=True if default_key == key else False)] for key in keys_list
        ], title=title, key=frame_key, tooltip=tooltip, relief=PySG.RELIEF_FLAT)]

    def _set_space_layout(self):
        # layout = []
        # for group_radio in \
        #         self._build_radios_layout(
        #             default_key=self._source_server.space_id, items_dict=self._source_spaces,
        #             title="Source Octopus server spaces", frame_key="source_spaces") \
        #         + self._build_radios_layout(
        #             default_key=self._config.space_id, items_dict=self._spaces, title="Octopus server spaces",
        #             frame_key="spaces"):
        #     layout.extend([group_radio])
        # layout.append([PySG.Button(MainGUI.PREV), PySG.Button(MainGUI.NEXT), PySG.Button(MainGUI.EXIT)])
        # return layout
        return [
            self._build_radios_layout(
                default_key=self._source_server.space_id, items_dict=self._source_spaces,
                title="Source Octopus server spaces", frame_key="source_spaces", key_prefix="source_"),
            self._build_radios_layout(
                default_key=self._config.space_id, items_dict=self._spaces, title="Octopus server spaces",
                frame_key="spaces"),
            [PySG.Button(MainGUI.PREV), PySG.Button(MainGUI.NEXT), PySG.Button(MainGUI.EXIT)]
        ]

    def _set_gui(self):
        PySG.theme(self._config.gui_theme)  # Add a touch of color
        action_window = MainGUI._set_window(layout=self._set_action_layout())
        submit_window_active = space_window_active = server_window_active = False
        action_event = None
        server_window = None
        space_window = None
        submit_window = None

        while True:
            if not server_window_active and not space_window_active:
                action_event, action_values = action_window.read()
                print(action_event)
                print(action_values)
                self._process_action(actions_dict=action_values)
                if action_event in (PySG.WIN_CLOSED, MainGUI.EXIT):
                    break

            if not server_window_active and not space_window_active and action_event == MainGUI.NEXT:
                server_window_active = True
                action_window.hide()
                server_window = MainGUI._set_window(layout=self._set_servers_layout())

            if server_window_active:
                server_event, server_values = server_window.read()
                print(server_event)
                print(server_values)
                self._process_server(server_dict=server_values)
                if server_event == MainGUI.PREV:
                    server_window_active = False
                    server_window.close()
                    action_window.un_hide()
                elif server_event == MainGUI.NEXT:
                    self._get_spaces()
                    if not self._spaces or self._config.action in Actions.MIGRATION_LIST \
                            and not self._source_spaces:
                        continue
                    server_window_active = False
                    server_window.hide()
                    space_window_active = True
                    space_window = MainGUI._set_window(layout=self._set_space_layout())
                    # submit_layout = [[PySG.Text("More options")],
                    #                  [PySG.Button(MainGUI.PREV), PySG.Button(MainGUI.EXIT)]]
                    # space_window = MainGUI._set_window(layout=self._set_space_layout())
                elif server_event in (PySG.WIN_CLOSED, MainGUI.EXIT):
                    server_window.close()
                    break

            # if not space_window_active and server_event == MainGUI.NEXT:
            #     space_window_active = True
            #     server_window.hide()
            #     space_window = MainGUI._set_window(layout=self._set_space_layout())

            if space_window_active:
                space_event, space_values = space_window.read()
                print(space_event)
                print(space_values)
                # self._process_space(space_dict=space_values)
                if space_event == MainGUI.PREV:
                    space_window_active = False
                    space_window.close()
                    server_window.un_hide()
                    server_window_active = True
                    self._clear_spaces()
                elif space_event == MainGUI.NEXT:
                    # self._get_spaces()
                    # if not self._spaces or self._config.action in Actions.MIGRATION_LIST \
                    #         and not self._source_spaces:
                    #     continue
                    submit_window_active = True
                    space_window_active = False
                    space_window.hide()
                    submit_layout = [[PySG.Text("More options")],
                                     [PySG.Button(MainGUI.PREV), PySG.Button(MainGUI.EXIT)]]
                    submit_window = MainGUI._set_window(layout=submit_layout)
                elif space_event in (PySG.WIN_CLOSED, MainGUI.EXIT):
                    space_window.close()
                    break

            if submit_window_active:
                submit_event, submit_values = submit_window.read()
                if submit_event == MainGUI.PREV:
                    submit_window.close()
                    submit_window_active = False
                    space_window_active = True
                    space_window.un_hide()
                elif submit_event in (PySG.WIN_CLOSED, MainGUI.EXIT):
                    submit_window.close()
                    break

        action_window.close()


if __name__ == "__main__":
    main_gui = MainGUI()
