# app_information.py: retrieves information about the ML app being run using the new app format (as of 8/8/2019).
# also, this module now serves as a consolidation of all the app-info related functions.
import os
from . import utils

class AppInfo():
    def __init__(self, config, app_path, box_info):
        self.config = config
        self.app_name = self._get_app_name(app_path)
        self.target = os.path.basename(app_path)

        if not self.app_name:
            utils.user_error("could not find a match between path='{}' and an app defined in the XT config file".format(app_path))

        self._set_app_info(box_info)

    def _get_app_name(self, app_path):
        match_name = None
        app_path = app_path.lower().replace("\\", "/")
        #print("app_path=", app_path)

        # find app with matching "match-path" property
        apps = self.config.get("apps")

        for app_name, app_value in apps.items():
            for key, value in app_value.items():
                if key == "match-path":
                    value = value.lower().replace("\\", "/")
                    if not value or value in app_path:
                        match_name = app_name
                        break
            
            if match_name:
                break

        return match_name

    def _create_default_prep_script(self, box_os):
        prep_script = []
        conda_env = utils.get_conda_env()
        
        if box_os == "windows":
            if conda_env:
                prep_script += "call conda activate {}".format(conda_env)
        else:
            if conda_env:
                prep_script += "conda activate {}".format(conda_env)
            
        return prep_script

    def _set_app_info(self, box_info):
        self.exper_name = None
        self.prep = None
        self.parent_prep = None
        self.box_class = box_info.box_class

        apps = self.config.get("apps")
        if not self.app_name in apps:
            utils.internal_error("app_name not found in config: {}".format(self.app_name))

        app_dict = apps[self.app_name]
        self.exper_name = self.config.get("general", "experiment")

        if not self.exper_name:
            if "experiment" in app_dict:
                self.exper_name = app_dict["experiment"]
            else:
                self.exper_name = ""

        if "prep" in app_dict:
            script_dict = app_dict["prep"]
            if self.box_class in script_dict:
                self.prep = script_dict[self.box_class]

        if "parent-prep" in app_dict:
            script_dict = app_dict["parent-prep"]
            if self.box_class in script_dict:
                self.parent_prep = script_dict[self.box_class]

    def get_prep_script(self, prep_stage="combined"):
        prep_script = None

        if prep_stage == "parent":
            # PARENT
            prep_script = self.parent_prep
        elif prep_stage == "child":
            # CHILD
            prep_script = self.prep

            if not prep_script:
                prep_script = self._create_default_prep_script(self.box_os)
                print("dynamic prep_script created: {}".format(self.prep))

        else:
            # combined
            #print("self.prep=", self.prep, ", self.parent_prep=", self.parent_prep)
            if self.prep:
                if self.parent_prep:
                    prep_script = self.parent_prep + self.prep
                else:
                    prep_script = self.prep
            else:
                prep_script = self.parent_prep

        if prep_script:
            conda_env = utils.get_conda_env()
            prep_script = [cmd.replace("$CURRENT_CONDA_ENV", conda_env) for cmd in prep_script]
            prep_script = [cmd.replace("$XT_TARGET_FILE", self.target) for cmd in prep_script]

        #print("get_prep_script: app_name=", self.app_name, ", prep_stage=", prep_stage, ", prep_script=", prep_script)
        return prep_script

