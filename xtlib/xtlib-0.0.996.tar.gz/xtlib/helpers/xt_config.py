# xtConfig.py: reads and writes the config.toml file, used to persist user settings for XT

import os
import toml
import shutil

from .. import utils as utils 
from .dot_dict import DotDict

class XTConfig():

    def __init__(self, fn=None, create_if_needed=False):
        self.create_if_needed = create_if_needed
        self.data = self.read_config(fn)

    def name_exists(self, group, name):
        return group in self.data and name in self.data[group]
        
    def warning(self, *msg_args):
        msg = "WARNING: xt_config file -"
        for arg in msg_args:
            msg += " " + str(arg)
        if self.get("general", "raise", suppress_warning=True):
            utils.user_error(msg)
        else:
            print(msg)

    # use "*" to require dict_key and default_value to be a named arguments
    def get(self, group, name=None, dict_key=None, default_value=None, suppress_warning=False, group_error=None, 
        prop_error=None, key_error=None):
        
        value = default_value

        if group in self.data:
            value = self.data[group]
            if name:
                if name in value:
                    value = value[name]
                    if dict_key:
                        if dict_key in value:
                            value = value[dict_key]
                        else:
                            if key_error:
                                utils.user_error(key_error)
                            if not suppress_warning:
                                self.warning("GET option dict_key not found: ", group, name, dict_key, default_value)
                            value = default_value
                else:
                    if prop_error:
                        utils.user_error(prop_error)
                    if not suppress_warning:
                        self.warning("GET option not found: ",  group, name, dict_key, default_value)
                    value = default_value
        else:
            if group_error:
                utils.user_error(group_error)
            if not suppress_warning:
                self.warning("GET option GROUP not found: ", group, name, dict_key, default_value)
            value = default_value
        return value

    # use "*" to require dict_key and value to be a named arguments
    def set(self, group, name, *, dict_key=None, value=None, suppress_warning=False):
        if group in self.data:
            gv = self.data[group]
            if name in gv:
                if dict_key:
                    obj = gv[name]
                    if not dict_key in obj:
                        if not suppress_warning:
                            self.warning("SET option dict_key not found: ", group, name, dict_key, value)
                    #print("set: obj=", obj, ", dict_key=", dict_key, ", value=", value)
                    obj[dict_key] = value
                    #print("set: post obj=", obj)
                else:
                    gv[name] = value
            else:
                if not suppress_warning:
                    self.warning("SET option name not found: ", group, name, dict_key, value)
                gv[name] = value
        else:
            raise Exception("SET option group not found: ", group, name, dict_key, value)
        
    def read_config(self, fn=None):
        if fn is None:
            config_dir = utils.get_xthome_dir() 
            utils.ensure_dir_exists(config_dir)
            fn = utils.get_config_fn()  

        if not os.path.exists(fn):
            if self.create_if_needed:
                print("XT config file not found; creating it from default settings...")
                file_dir = os.path.dirname(os.path.realpath(__file__))
                from_fn = file_dir + "/default_config.toml"
                shutil.copyfile(from_fn, fn)
            else:
                utils.user_error("XT config file doesn't exist: {}".format(fn))

        # read config file
        try:
            config = toml.load(fn)
        except Exception as e:
            raise Exception (f"The config file '{fn}' is not valid TOML, error: {e}")

        return config

def get_merged_config(create_if_needed=True):
    config = XTConfig(create_if_needed=create_if_needed)

    # apply local override file, if present
    fn_overrides = utils.OVERRIDES_FN
    if os.path.exists(fn_overrides):
        overrides = XTConfig(fn=fn_overrides, create_if_needed=False)
        #print("config.data['apps']=", config.data['apps'].keys())

        # note: a simple dict "update()" is too blunt; we need a fine-grained key/value update
        config_data = config.data

        for section_name, section_value in overrides.data.items():
            if not section_name in config_data:
                config_data[section_name] = {}
            for key, value in section_value.items():
                if isinstance(value, dict):
                    if not key in config_data[section_name]:
                        config_data[section_name][key] = {}
                    for inner_key, inner_value in value.items():
                        #print("overridding: [{}.{}] {} = {}".format(section_name, key, inner_key, inner_value))
                        config_data[section_name][key][inner_key] = inner_value
                else:
                    #print("overridding: [{}] {} = {}".format(section_name, key, value))
                    config_data[section_name][key] = value

    return config
