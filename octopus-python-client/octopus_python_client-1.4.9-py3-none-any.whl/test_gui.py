import sys
import tkinter as tk
from tkinter import ttk

from octopus_python_client.actions import Actions
from octopus_python_client.common import Common
from octopus_python_client.config import Config


class ActionsWidgets(tk.Frame):
    def __init__(self, parent, common: Common, source: Common):
        super().__init__(parent)
        self.common = common
        self.source = source
        self.select_action = tk.StringVar()

        self.update_step()

    def update_step(self):
        tk.Label(self, text="Action selection", bd=2, relief="groove").pack(side="top", fill="x")
        self.select_action.set(self.common.config.action)
        for action, description in Actions.ACTIONS_DICT.items():
            radio = tk.Radiobutton(self, text=f"{action} ({description})", variable=self.select_action, value=action,
                                   justify=tk.LEFT, command=self.select_action)
            radio.pack(anchor=tk.W)

    def select_action(self):
        self.common.config.action = self.select_action.get()

    def save_config(self):
        self.common.config.save_config()


class ServersWidgets(tk.Frame):
    def __init__(self, parent, common: Common, source: Common):
        super().__init__(parent)

        self.common = common
        self.source = source
        self.local_data = tk.StringVar()
        self.target_variables = {}
        self.source_variables = {}
        self.update_step()

    def update_step(self):
        self.target_variables = {}
        self.source_variables = {}
        tk.Label(self, text=f"{self.common.config.action} ({Actions.ACTIONS_DICT.get(self.common.config.action)})",
                 bd=2, relief="groove").grid(sticky=tk.W)
        if self.common.config.action in Actions.MIGRATION_LIST:
            self.source_variables = self.set_server_frame(config=self.source.config)
            # 'The source server data is loaded from local files, not directly from server'
            tk.Checkbutton(self, text="The source Octopus data is loaded from local files, not from Octopus server",
                           variable=self.local_data).grid(sticky=tk.EW)
            self.local_data.set(self.source.config.local_data)
            ttk.Separator(self, orient=tk.HORIZONTAL).grid(sticky=tk.EW)
            tk.Label(self, text=f"\u21D3     \u21D3     \u21D3     \u21D3     \u21D3      {self.common.config.action}"
                                f"      \u21D3     \u21D3     \u21D3     \u21D3     \u21D3",
                     bd=2, relief="groove").grid(sticky=tk.EW)
            ttk.Separator(self, orient=tk.HORIZONTAL).grid(sticky=tk.EW)
        self.target_variables = self.set_server_frame(config=self.common.config)

    def set_server_frame(self, config: Config):
        server_frame = tk.Frame(self)

        title = f"Octopus {'source' if config.is_source_server else 'target'} server"
        tk.Label(server_frame, text=title).grid(row=0, column=0, sticky=tk.EW, columnspan=8)

        tk.Label(server_frame, text="Server endpoint (must end with /api/)") \
            .grid(row=1, column=0, sticky=tk.E, columnspan=4)
        endpoint_variable = tk.StringVar()
        tk.Entry(server_frame, width=40, textvariable=endpoint_variable) \
            .grid(row=1, column=4, columnspan=4, sticky=tk.W)
        endpoint_variable.set(config.endpoint if config.endpoint else "")

        tk.Label(server_frame, text="API-KEY (must start with API-)").grid(row=2, column=0, sticky=tk.E, columnspan=4)
        api_key_variable = tk.StringVar()
        tk.Entry(server_frame, width=40, show="*", textvariable=api_key_variable) \
            .grid(row=2, column=4, columnspan=4, sticky=tk.W)
        api_key_variable.set(config.api_key if config.api_key else "")

        tk.Label(server_frame, text="user_name/password NOT used if API-KEY exists: ") \
            .grid(row=3, column=0, sticky=tk.E, columnspan=4)

        tk.Label(server_frame, text="user_name").grid(row=3, column=4, sticky=tk.W, columnspan=1)
        user_name_variable = tk.StringVar()
        tk.Entry(server_frame, width=10, textvariable=user_name_variable) \
            .grid(row=3, column=5, sticky=tk.W, columnspan=1)
        user_name_variable.set(config.user_name if config.user_name else "")

        tk.Label(server_frame, text="password").grid(row=3, column=6, columnspan=1, sticky=tk.E)
        password_variable = tk.StringVar()
        tk.Entry(server_frame, width=10, show="*", textvariable=password_variable) \
            .grid(row=3, column=7, sticky=tk.E, columnspan=1)
        password_variable.set(config.password if config.password else "")

        tk.Label(server_frame, text="Local path to store Octopus data") \
            .grid(row=4, column=0, sticky=tk.E, columnspan=4)
        work_path_variable = tk.StringVar()
        tk.Entry(server_frame, width=40, textvariable=work_path_variable) \
            .grid(row=4, column=4, sticky=tk.W, columnspan=4)
        work_path_variable.set(config.work_path if config.work_path else "")

        tk.Label(server_frame, text="Folder to store Octopus data for one server") \
            .grid(row=5, column=0, sticky=tk.E, columnspan=4)
        octopus_name_variable = tk.StringVar()
        tk.Entry(server_frame, width=40, textvariable=octopus_name_variable) \
            .grid(row=5, column=4, sticky=tk.W, columnspan=4)
        octopus_name_variable.set(config.octopus_name if config.octopus_name else "")

        server_frame.grid(sticky=tk.W)
        return {Config.ENDPOINT: endpoint_variable, Config.API_KEY: api_key_variable,
                Config.USER_NAME: user_name_variable, Config.PASSWORD: password_variable,
                Config.WORK_PATH: work_path_variable, Config.OCTOPUS_NAME: octopus_name_variable}

    def save_config(self):
        if self.source_variables:
            for key, variable in self.source_variables.items():
                self.source_variables[key] = variable.get()
            self.source.config.__dict__.update(self.source_variables)
            self.source.config.local_data = True if self.local_data.get() == "1" else False
            self.source.config.save_config()
        for key, variable in self.target_variables.items():
            self.target_variables[key] = variable.get()
        self.common.config.__dict__.update(self.target_variables)
        self.common.config.save_config()


class SpacesWidgets(tk.Frame):
    def __init__(self, parent, common: Common, source: Common):
        super().__init__(parent)

        header = tk.Label(self, text="This is step 3", bd=2, relief="groove")
        header.pack(side="top", fill="x")

    def save_config(self):
        pass


class SubmitWidgets(tk.Frame):
    def __init__(self, parent, common: Common, source: Common):
        super().__init__(parent)

        header = tk.Label(self, text="This is step 4", bd=2, relief="groove")
        header.pack(side="top", fill="x")

    def save_config(self):
        pass


class Wizard(tk.Frame):
    def __init__(self, parent, common: Common, source: Common):
        super().__init__(parent)

        self.common = common
        self.source = source

        self.current_step_index = None
        self.current_step_widgets = None
        self.steps = [ActionsWidgets, ServersWidgets, SpacesWidgets, SubmitWidgets]

        self.button_frame = tk.Frame(self, bd=1, relief="raised")
        self.back_button = tk.Button(self.button_frame, text="<< Back", command=self.back)
        self.next_button = tk.Button(self.button_frame, text="Next >>", command=self.next)
        self.submit_button = tk.Button(self.button_frame, text="Submit", command=self.submit)
        self.button_frame.pack(side="bottom", fill="x")

        self.content_frame = tk.Frame(self)
        self.show_step(0)
        self.content_frame.pack(side="top", fill="both", expand=True)

    def show_step(self, step):

        if self.current_step_widgets is not None:
            # remove current step
            self.current_step_widgets.pack_forget()

        self.current_step_index = step
        self.current_step_widgets = self.steps[step](self.content_frame, common=self.common, source=self.source)
        self.current_step_widgets.pack(fill="both", expand=True)

        if step == 0:
            # first step
            self.back_button.pack_forget()
            self.next_button.pack(side="right")
            self.submit_button.pack_forget()

        elif step == len(self.steps) - 1:
            # last step
            self.back_button.pack(side="left")
            self.next_button.pack_forget()
            self.submit_button.pack(side="right")

        else:
            # all other steps
            self.back_button.pack(side="left")
            self.next_button.pack(side="right")
            self.submit_button.pack_forget()

    def next(self):
        self.current_step_widgets.save_config()
        self.show_step(self.current_step_index + 1)

    def back(self):
        self.current_step_widgets.save_config()
        self.show_step(self.current_step_index - 1)

    def submit(self):
        self.current_step_widgets.save_config()
        sys.exit()


class MainGUI:
    SOURCE_SERVER_JSON = "source_server.json"

    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.config = Config()
        self.common = Common(config=self.config)
        self.source_server = Config(configuration_file_name=MainGUI.SOURCE_SERVER_JSON, is_source_server=True)
        self.source_common = Common(config=self.source_server)

    def set_gui(self):
        window = tk.Tk()
        window.title('Octopus python client')
        window.option_add("*font", "calibri 16")
        window["bg"] = "black"

        # window.geometry('800x600')

        wiz = Wizard(window, common=self.common, source=self.source_common)
        wiz.pack()

        window.mainloop()


if __name__ == "__main__":
    MainGUI().set_gui()
