# cmd_line.py: implements the command line version of the XT tool
'''
General design: handling all of the option and command parsing for XT command line too
in this module.  The functionality (without any parser ties) resides in xt_client.
'''
import os
import sys
import json
import math
import time
import arrow
import socket
import argparse
import platform
import datetime
import subprocess
import numpy as np

from time import sleep
from fnmatch import fnmatch
from collections import OrderedDict
from matplotlib import pyplot as plt

from .helpers import xt_config
from .helpers.dot_dict import DotDict
from .helpers.scanner import Scanner
from .helpers.key_press_checker import KeyPressChecker
from . import help
from . import utils as utils 
from .client import Client
from .store import Store
from .list_builder import ListBuilder   
from .hp_process import HPProcess
from xtlib.cmd_core import CmdCore
from .hyperex import HyperparameterExplorer
from . import box_information

#USER_SETTINGS = "~/.xt/user_settings.json"

class CmdLine():
    def __init__(self):
        self.explicit_options = {}
        self.core = None
        self.client = None
        self.config = None

    def build_default_options(self):
        # xt options are 1 of 4 types:
        #   flag, boolean, number, string
        # flags and booleans don't require an "=value" after then, the others do.
        bool_options = [
            # status flags
            "active", "finished", "queued", "spawning", "running", "completed", "error", "killed", "aborted", 
            "allocating", "unknown",
            # other
            "help", "monitor", "reverse", "hold", "flat", "diagnostics", "boxout", 
            "dry-run", "overwrite", "local", "repair", "raise", "timing", "attach", "keep-name", "demand-mode",
            "auto-start", "tqdm-enabled", "login", "xtlib-capture", "distributed"]

        other_options = [
            "log", "scrape", "workspace", "capture", "notes", "framework", "vm-size", "runs", "tags", "sort", 
            "box", "pool", "experiment", "max-runs", "repeat", "detail", "escape", "store-type", "app", 
            "max-width", "precision", "description", "vm-size", "azure-image", "nodes", "low-pri",
            "job", "subdirs", "hp-config", "arg-prefix", "hx-cache-dir", "resume", "first", "last", "hx-metric",
            "aggregate-dest", "runs-cache", "search-type", "xt-config", "omit", "before-files", "after-files"]

        opt1 = {opt:True for opt in bool_options }
        opt2 = {opt:False for opt in other_options }
        options = {**opt1, **opt2}

        # define all options in self.config (if not already defined there)
        for key, value in options.items():
            if (not self.config.name_exists("core", key)) and (not self.config.name_exists("general", key)):
                #print("set option only config: key=", key, ", value=", None)
                self.config.set("general", key, value=None, suppress_warning=True)

        self.bool_options = bool_options
        self.options = options

    def is_boolean_value(self, option, tok):
        value = tok
        is_bool = False
        if tok and tok in self.bool_options:
            is_bool = tok.lower() in ["true", "false", "on", "off", "0", "1"]
            if is_bool:
                value = (tok.lower() in ["true", "on", "1"])
        
        return is_bool, value

    def set_option_value(self, option, value):
        #print("setting option=", option, ", to value=", value)

        # convert strings to numbers, when possible
        if isinstance(value, str):
            value = utils.make_numeric_if_possible(value)

        # record as an explicit option
        self.explicit_options[option] = value

        # merge with config info (look in core, reports, then general)
        groups = ["core", "reports", "azure", "hp-search", "azure-container-registry"]
        found = False

        for group in groups:
            if self.config.name_exists(group, option):
                self.config.set(group, option, value=value)
                found = True
                break

        if not found:
            self.config.set("general", option, value=value)

    def parse_option(self, tok):
        options = self.options

        #print("option=", option)
        option = tok[2:]     # stip off "--"

        match = self.match(option, options)
        if not match:
            utils.user_error(f"unrecognized option: --{option}")

        option = match
        #ion=", option)
        #print("options[option]=", options[option])

        tok = self.scanner.scan()        # skip over option name
        optional_value = (options[option] == True)
        #print("option=", option, ", optional_value=", optional_value)

        # the "=" is optional, skip over it if it exists
        if tok == "=":
            tok = self.scanner.scan()
            optional_value = False

        is_bool, value = self.is_boolean_value(option, tok)
        #print("option=", option, ", is_bool=", is_bool, ", value=", value)

        if optional_value:
            # parse optional boolean value
            if is_bool:
                self.set_option_value(option, value)
                tok = self.scanner.scan()       
            else:
                # mentioning a flag/bool without a value sets it to True
                self.set_option_value(option, True)
        else:
            # parse a rquired boolean/string/number value
            if is_bool:
                self.set_option_value(option, value)
            else:
                if not value and option == "workspace":
                    utils.user_error("--ws option must be set to a workspace name; value=" + str(value))
                self.set_option_value(option, tok)
            tok = self.scanner.scan()               

            #options[option] = value  

        return tok

    def parse_config_cmd(self):
        # let user edit the CONFIG file
        tok = self.scanner.scan()         # skip over "config"

        # process any in-line options for this command            
        #self.process_named_options(tok)

        # manual parsing for this EARLY cmd
        #use_local = self.config.get("general", "local")

        use_local = False
        if tok in ["--local", "local"]:
            use_local = True
        elif tok:
            utils.user_error("unrecognized 'xt config' option: {}".format(tok))

        if use_local:        
            fn = utils.OVERRIDES_FN
        else:
            fn = utils.get_config_fn()

        edit = True
        if not os.path.exists(fn):
            print("the config file doesn't exist: {}".format(fn))
            answer = input("OK to create?  (y/n) [y]: ")
            if answer in ["", "y"]:
                # create new LOCAL file
                with open(fn, "w") as newfile:
                    newfile.write("# local xt_config_overrides.toml file\n\n")
                    newfile.write("#[general]\n")
                    newfile.write('#workspace = "my_ws_for_this_project"\n')
            else:
                edit = False

        if edit:
            print(f"invoking your default .toml editor on: {fn}")
            utils.open_file_with_default_app(fn)

    def parse_create_workspace_cmd(self, tok):
        ws_id = self.scanner.scan()     # sskip over "workspace" keyword
        if not ws_id:
            utils.user_error("must specified workspace name to be created")
        tok = self.scanner.scan()       # skip over ws name

        # process any in-line options for this command            
        self.process_named_options(tok)

        self.store.create_workspace(ws_id)
        print("workspace created: " + ws_id)

    def parse_delete_workspace_cmd(self, tok):
        ws_id = self.scanner.scan()          # skip over "workspace" keyword
        tok = self.scanner.scan()          # skip over ws name

        # process any in-line options for this command            
        self.process_named_options(tok)

        if not self.store.does_workspace_exist(ws_id):
            print("workspace not defined: " + ws_id)
        else:
            names = self.store.get_run_names(ws_id)
            #print("names=", names)

            count = len(names)

            if ws_id == self.ws:
                print("fyi: this is current default workspace")

            answer = input("Enter 'delete' to confirm deletion of workspace {} ({} runs): ".format(ws_id, count))
            if answer == "delete":
                self.store.delete_workspace(ws_id)
                print("workspace deleted: " + ws_id)

                # if ws_id == self.ws:
                #     self.config.set("general", "workspace", value="")
                #     self.ws = ""
                #     self.save_user_settings()

                #     print("please use the 'xt workspace' cmd to set a new current workspace")
            else:
                print("workspace not deleted")


    def parse_list_workspaces_cmd(self):
        tok = self.scanner.scan()     # skip over ws keyword

        # process any in-line options for this command            
        self.process_named_options(tok)

        detail = self.config.get("general", "detail", default_value="names")
        show_counts = detail=="counts"

        names = self.store.get_workspace_names()
        #print("names=", names)
        fmt_workspace = utils.format_store(self.store_type)
        print(f"\n{fmt_workspace} workspaces:")
        
        # print HEADERS
        if show_counts:
            print(f'  {"NAME":20.20s} {"RUNS":>8s}\n')  

            # print VALUES for each record
            for name in names:
                exper_count = len(self.store.get_run_names(name))
                if len(name) > 20:
                    name = name[0:18] + "..."
                print(f'  {name:20.20s} {exper_count:>8d}')
        else:
            for name in names:
                print(f'  {name:20.20s}')

    def get_first_last_filtered_names(self, names, top_adjust=0, bot_adjust=0):
        first_count = self.config.get("general", "first")
        last_count = self.config.get("general", "last")

        if first_count:
            names = names[:first_count + top_adjust]
        if last_count:
            names = names[-(last_count + bot_adjust):]

        return names            

    def parse_list_jobs_cmd(self):
        tok = self.scanner.scan()     # skip over jobs keyword
        wildcard_name = None

        if tok and not self.is_option(tok):
            wildcard_name = tok
            tok = self.scanner.scan()     # skip over wildcard

        # process any in-line options for this command            
        self.process_named_options(tok)

        # get all job names
        names = self.store.get_job_names()

        if wildcard_name:
            # show detail of matching jobs
            names = [name for name in names if fnmatch(name, wildcard_name)]
            names = self.get_first_last_filtered_names(names)

            print("job definitions:")
            for name in names:
                text = self.store.read_job_info_file(name)
                dd = json.loads(text)
                print("  {}: {}".format(name, dd))
        else:
            print("jobs in store:")
            names = self.get_first_last_filtered_names(names)

            for name in names:
                print("  " + str(name))

    def parse_list_boxes_cmd(self):
        tok = self.scanner.scan()     # skip over boxes keyword
        wildcard_name = None

        if tok and not self.is_option(tok):
            wildcard_name = tok
            tok = self.scanner.scan()     # skip over wildcard

        # process any in-line options for this command            
        self.process_named_options(tok)

        # get all box names
        names = list(self.config.get("boxes").keys())

        if wildcard_name:
            # show detail of matching boxes
            names = [name for name in names if fnmatch(name, wildcard_name)]
            names = self.get_first_last_filtered_names(names)

            print("box definitions:")
            for name in names:
                dd = self.config.get("boxes", name)
                print("  {}: {}".format(name, dd))
        else:
            print("boxes defined in config file:")
            names = self.get_first_last_filtered_names(names)

            for name in names:
                print("  " + str(name))

    def parse_list_pools_cmd(self):
        tok = self.scanner.scan()     # skip over pools keyword
        wildcard_name = None

        if tok and not self.is_option(tok):
            wildcard_name = tok
            tok = self.scanner.scan()     # skip over wildcard

        # process any in-line options for this command            
        self.process_named_options(tok)

        # get all pool names
        names = list(self.config.get("pools").keys())

        if wildcard_name:
            # show detail of matching pools
            names = [name for name in names if fnmatch(name, wildcard_name)]
            names = self.get_first_last_filtered_names(names)

            print("pool definitions:")
            for name in names:
                dd = self.config.get("pools", name)
                print("  {}: {}".format(name, dd))
        else:
            print("pools defined in config file:")
            names = self.get_first_last_filtered_names(names)

            for name in names:
                print("  " + str(name))

    def parse_list_exper_cmd(self):
        exper_wildcard = None
        tok = self.scanner.scan()     # skip over exper
        if tok and not self.is_option(tok):
            exper_wildcard = tok
            tok = self.scanner.scan()     # skip over wildcard

        # process any in-line options for this command            
        self.process_named_options(tok)

        builder = ListBuilder(self.config, self.store, self.client)

        #print("experiments for workspace: " + self.ws + "\n")

        detail = self.config.get("general", "detail", default_value="names")
        #print("detail=", detail)

        if detail == "cols":
            lines = builder.build_grouped(exper_wildcard)
        else:
            lines = builder.build_exper_summary(exper_wildcard, detail=="counts")

        if lines:
            # filter experiment lines
            lines = self.get_first_last_filtered_names(lines)

            for line in lines:
                print(line)

        tok = self.scanner.scan()
        return tok

    def is_option(self, tok):
        ''' return True if tok is the name of an option
        '''
        found = False

        if tok:
            if tok.startswith("--"):
                found = True
            else:
                for option in self.options:
                    if self.match(tok, option):
                        found = True
                        break

        return found

    def process_named_options(self, tok):
        '''
        now that cmd keywords and main value have been processed, parse any remaining
        named options and store in config data, for cmd to access as it runs.
        '''
        while tok:
            if tok.startswith("--"):
                # remove optional "--"
                tok = tok[2:]

            #print("tok=", tok)
            match = False

            for option in self.options:
                match = self.match(tok, option)
                if match:
                    break

            if not match:
                utils.user_error("unrecognized command option: {}".format(tok))

            tok = self.scanner.scan()       # skip over "match" keyword
            #print("match=", match, ", next tok=", tok)

            if not tok:
                self.set_option_value(match, True)
            elif (tok == "="):
                value = self.scanner.scan()     # skip over "="
                is_bool, value = self.is_boolean_value(match, value)
                #print("option=", option, ", is_bool=", is_bool, ", value=", value)

                self.set_option_value(match, value)
                tok = self.scanner.scan()             # skip over option value
            elif not self.is_option(tok):
                # not a recognized option name, assume it is a value 
                self.set_option_value(match, tok)
                tok = self.scanner.scan()             # skip over option value

        # now that options have been updated, should update our cached options
        self.on_options_changed()

    def parse_view_console_cmd(self, tok):
        if self.match(tok, "console"):
            fn = "after/console.txt"
        elif self.match(tok, "stdout"):
            fn = "after/stdout.txt"
        else:       # stderr
            fn = "after/stderr.txt"

        run_name = self.scanner.scan()     # skip over "console" keyword
        if not run_name:
            utils.user_error("must specify a run name")

        tok = self.scanner.scan()

        # process any in-line options for this command            
        self.process_named_options(tok)

        # NOTE: validate_run_name() call must be AFTER we call process_named_options()
        ws, run_name, full_run_name = utils.validate_run_name(self.store, self.ws, run_name)

        if not self.store.does_run_file_exist(ws, run_name, fn):
            print("run '{}' has no file'{}'".format(full_run_name, fn))
        else:
            print("{} for {}:\n".format(fn, full_run_name))

            text = self.store.read_run_file(ws, run_name, fn)
            text = utils.make_text_display_safe(text)
            print(text)

    def parse_view_log_cmd(self, tok):
        run_name = self.scanner.scan()     # skip over "log" keyword
        if not run_name:
            utils.user_error("must specify a run name")

        tok = self.scanner.scan()

        # process any in-line options for this command            
        self.process_named_options(tok)

        if self.match(run_name, "controller"):
            # view CONTROLLER LOG from specified box
            box = self.box
            self.client.init_controller(box)
            text = self.client.get_controller_log()
            print("box={}, controller log:".format(box.upper()))
            print(text)
        else:
            # view RUN LOG of run
            # NOTE: validate_run_name() call must be AFTER we call process_named_options()
            ws, run_name, full_run_name = utils.validate_run_name(self.store, self.ws, run_name)
            records = self.store.get_run_log(ws, run_name)
            print("log for {}:\n".format(full_run_name))

            for record in records:
                print(record)

    def parse_plot_command(self):
        tok = self.scanner.scan()     # skip over "plot" keyword

        run_names, tok = self.parse_run_name_list(tok, True)

        if not run_names:
            utils.user_error("must specify at least one run name")

        # process any in-line options for this command            
        self.process_named_options(tok)

        # TODO: merge metrics from multiple runs
        if len(run_names) > 1:
            utils.user_error("multiple runs not yet supported for plotting")
        full_run_name = run_names[0]    
        ws, run_name = full_run_name.split("/")

        records = self.store.get_run_log(ws, run_name)
        metric_sets = utils.build_metrics_sets(records)

        for ms in metric_sets:
            keys = ms["keys"]
            if len(keys) == 1 and keys[0].lower() == "epoch":
                # skip isolated epoch reporting
                continue

            # remove x-col names from y_cols
            x_names = ["epoch", "step", "iter"]
            x_col = None
            for xn in x_names:
                if xn in keys:
                    if not x_col:
                        x_col = xn
                    keys.remove(xn)

            loss_keys = [key for key in keys if "loss" in key.lower()]
            non_loss_keys = [key for key in keys if not "loss" in key.lower()]

            if loss_keys:
                self.plot_from_records(ms["records"], loss_keys, x_col)

            if non_loss_keys:
                self.plot_from_records(ms["records"], non_loss_keys, x_col)

    def plot_from_records(self, records, y_cols, x_col=None):
        from matplotlib.ticker import MaxNLocator
        from pylab import figure, show

        fig = figure()
        ax = fig.add_subplot(111)
        colors = ["blue", "red", "green", "orange"]

        if x_col:
            x_values = [float(record[x_col]) for record in records]
            ax.set_xlabel(x_col)
        else:
            x_values = None

        for i, y_col in enumerate(y_cols):
            y_values = [float(record[y_col]) for record in records]
            #print("y_values=", y_values)

            num_y_ticks = 10

            ax.yaxis.set_major_locator(MaxNLocator(num_y_ticks))
            color = colors[i % len(colors)]

            if x_values:
                ax.plot(x_values, y_values, '-', ms=3, markerfacecolor=color, markeredgecolor=color, 
                    color=color, markeredgewidth=1, label=y_col)
            else:
                ax.plot(y_values, '-', ms=3, markerfacecolor=color, markeredgecolor=color, 
                    color=color, markeredgewidth=1, label=y_col)

            # ms=4, linewidth=1, markersize=4, mfc='none', mec="blue")    # , x_values)
            # x,y2, 'o', ms=14, markerfacecolor="None", markeredgecolor='red', markeredgewidth=5

            # # multiple line plot
            # plt.plot( 'x', 'y1', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
            # plt.plot( 'x', 'y2', data=df, marker='', color='olive', linewidth=2)
            # plt.plot( 'x', 'y3', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
            # plt.legend()

        #ax.set_ylabel(y_col)
        ax.legend()


        #if x_col:
        #    ax.x_label(x_col)

        show()

    def parse_view_metrics_cmd(self, tok):
        run_name = self.scanner.scan()     # skip over "metrics" keyword
        if not run_name:
            utils.user_error("must specify a run name")

        tok = self.scanner.scan()

        # process any in-line options for this command            
        self.process_named_options(tok)

        # NOTE: validate_run_name() call must be AFTER we call process_named_options()
        ws, run_name, full_run_name = utils.validate_run_name(self.store, self.ws, run_name)

        records = self.store.get_run_log(ws, run_name)
        print("metrics for {}:\n".format(full_run_name))

        metric_sets = utils.build_metrics_sets(records)
        for ms in metric_sets:
            lb = ListBuilder(self.config, self.store, self.client)
            text = lb.build_formatted_table(ms["records"], ms["keys"])
            print(text)

    def parse_run_name_list(self, tok, required=False):
        ''' returns a list of full run names (each of form: workspace/run)
        '''
        run_names = []
        #print("tok=", tok)

        # process unnamed optional values
        while tok:
            if not utils.is_well_formed_run_name(tok):
                break

            # NOTE: validate_run_name() call must be AFTER we call process_named_options()
            ws, run_name, full_name = utils.validate_run_name(self.store, self.ws, tok, True)
            if ws is None:
                break

            run_names.append(full_name)
            tok = self.scanner.scan()     # skip over run_name
            if tok == ",":
                tok = self.scanner.scan()     # skip over optional comma

        if not run_names and required:
            utils.user_error("At least one run name must be specified for this command")

        return run_names, tok

    def parse_list_runs_cmd(self):
        tok = self.scanner.scan()     # skip over "runs" keyword

        full_run_names, tok = self.parse_run_name_list(tok, False)

        # remove workspace from full_run_names 
        run_names = []
        actual_ws = None

        for full_run_name in full_run_names:
            ws, run_name = full_run_name.split("/")
            if actual_ws and actual_ws != ws:
                utils.user_error("Cannot mix run_names from different workspaces for this command")
            run_names.append(run_name)
            actual_ws = ws

        # process any in-line options for this command            
        self.process_named_options(tok)

        if not actual_ws:
            actual_ws = self.ws
            
        boxes_filter, pool_info, is_azure_pool, is_azure_box  = box_information.get_box_list(self.core, explicit_boxes_only=True)
        #print("boxes_filter=", boxes_filter)

        builder = ListBuilder(self.config, self.store, self.client)
        lines = builder.build_flat(actual_ws, run_names, boxes_filter)

        lines = self.get_first_last_filtered_names(lines, 2, 1)

        # print the list
        print("\n{} runs:".format(actual_ws.upper()))
        for line in lines:
            print(line)

        tok = self.scanner.scan()
        return tok

    def match(self, tok, keywords):
        match = None
        if tok:
            tok = tok.lower()
            if isinstance(keywords, str):
                keywords = [ keywords ]

            for kw in keywords:
                if kw.startswith(tok) and len(tok) >= min(4, len(kw)):
                    match = kw
                    break
        return match

    def parse_list_commands(self):
        tok = self.scanner.scan()        # skip over "list"

        if self.match(tok, ["run", "runs"]):
            self.parse_list_runs_cmd()        
        elif self.match(tok, ["experiments"]):
            self.parse_list_exper_cmd()        
        elif self.match(tok, ["job", "jobs"]):
            self.parse_list_jobs_cmd()        
        elif self.match(tok, ["ws", "workspaces"]):
            self.parse_list_workspaces_cmd()
        elif self.match(tok, ["box", "boxes"]):
            self.parse_list_boxes_cmd()
        elif self.match(tok, ["pools"]):
            self.parse_list_pools_cmd()
        elif self.match(tok, ["files"]):
            self.parse_list_files_cmd()
        else:
            if tok:
                utils.user_error("unrecognized list target: " + str(tok))     
            else:
                utils.user_error("what do you want to list?  try 'list exper' or 'list ws'")     

    def parse_view_commands(self):
        tok = self.scanner.scan()        # skip over "view"

        if self.match(tok, ["console", "stdout", "stderr", "output"]):
            self.parse_view_console_cmd(tok)        
        elif self.match(tok, ["log"]):
            self.parse_view_log_cmd(tok)        
        elif self.match(tok, ["metrics"]):
            self.parse_view_metrics_cmd(tok)        
        else:
            if tok:
                utils.user_error("unrecognized view target: " + str(tok))     
            else:
                utils.user_error("what do you want to view?  try 'view console'")     

    def parse_create_commands(self):
        tok = self.scanner.scan()        # skip over "create"
        if self.match(tok, ["ws", "workspace"]):
            self.parse_create_workspace_cmd(tok)        
        else:
            utils.user_error("unrecognized create target: " + str(tok))     

    def parse_delete_commands(self):
        tok = self.scanner.scan()        # skip over "delete"

        if self.match(tok, ["ws", "workspace"]):
            self.parse_delete_workspace_cmd(tok)        
        elif self.match(tok, ["file"]):
            self.parse_delete_file_cmd(tok)        
        else:
            utils.user_error("unrecognized delete target: " + str(tok))     

    def parse_docker_commands(self):
        tok = self.scanner.scan()        # skip over "docker"

        if self.match(tok, "login"):
            self.parse_docker_login_cmd()        
        elif self.match(tok, "logout"):
            self.parse_docker_logout_cmd()        
        elif self.match(tok, "run"):
            self.parse_python_or_run_cmd(tok, is_docker=True)        
        else:
            utils.user_error("unrecognized docker action: " + str(tok))     

    def get_scanner_arg_index(self, args):
        ''' calculate which argument the scanner is on'''
        text_index = self.scanner.index
        text = self.scanner.text
        index = 0

        for arg_index, arg in enumerate(args):
            index += (len(arg) + 1)
            if index >= text_index:
                break

        return arg_index

    def parse_extract_cmd(self):
        run_name = self.scanner.scan()     # skip over 'extract'

        dest_dir = self.scanner.scan()     # skip over run_name
        tok = self.scanner.scan()          # skip over output directory

        # process any in-line options for this command            
        self.process_named_options(tok)

        # NOTE: validate_run_name() call must be AFTER we call process_named_options()
        ws, run_name, full_run_name = utils.validate_run_name(self.store, self.ws, run_name)

        self.client.extract_run(ws, run_name, dest_dir)
        return tok

    def parse_cat_cmd(self):
        path = self.scanner.scan()     # skip over 'cat'
    
        if path:
            tok = self.scanner.scan()          # skip over path
        else:
            tok = path

        # process any in-line options for this command            
        self.process_named_options(tok)

        text = self.core.read_store_file(self.ws, path)
        print("")

    def parse_docker_login_cmd(self):
        tok = self.scanner.scan()     # skip over 'login'
    
        # process any in-line options for this command            
        self.process_named_options(tok)

        server = self.config.get("azure-container-registry", "login-server")
        username = self.config.get("azure-container-registry", "username")
        password = self.config.get("azure-container-registry", "password")

        text = self.core.docker_login(server, username, password)
        print(text)

    def parse_docker_logout_cmd(self):
        tok = self.scanner.scan()     # skip over 'logout'
    
        # process any in-line options for this command            
        self.process_named_options(tok)

        server = self.config.get("azure-container-registry", "login-server")
        
        text = self.core.docker_logout(server)
        print(text)

    def parse_dir_cmd(self):
        path = self.scanner.scan()     # skip over 'dir'
    
        if path:
            tok = self.scanner.scan()          # skip over path
        else:
            tok = path

        # process any in-line options for this command            
        self.process_named_options(tok)

        subdirs = self.config.get("general", "subdirs")

        dd = self.core.list_store_files(self.ws, path, subdirs)
        print("")
        print(dd["store_name"])

        for folder in dd["folders"]:
            print("\nDirectory of store:" + folder["folder_name"])
            print("")
            
            # find maximum size of files in this folder
            max_size = 0
            for fi in folder["files"]:
                size = fi["size"]
                max_size = max(size, max_size)

            max_size_str = "{:,d}".format(max_size)
            size_width = max(5, len(max_size_str))

            fmt_folder = "{:20s}  {:<99s}  {}".replace("99", str(size_width))
            fmt_file =   "{:20s}  {:>99,d}  {}".replace("99", str(size_width))
            #print("fmt_folder=", fmt_folder)

            for dir_name in folder["dirs"]:
                print(fmt_folder.format("", "<DIR>", dir_name))

            for fi in folder["files"]:
                size = fi["size"]
                name = fi["name"]
                dt = datetime.datetime.fromtimestamp(fi["modified"])
                dt = dt.strftime("%m/%d/%Y  %I:%M %p")
                print(fmt_file.format(dt, size, name))

    def parse_kill_cmd(self):
        tok = self.scanner.scan()   # skip over the "kill"
        run_names = None
        target_controller = False
        target_all_runs = False

        if tok == "controller":
            target_controller = True
            tok = self.scanner.scan()     # skip over all/controller keyword
        elif tok == "all":
            target_all_runs = True
            tok = self.scanner.scan()     # skip over all/controller keyword
        else:
            run_names, tok = self.parse_run_name_list(tok, True)

        # process any in-line options for this command
        #print("tok=", tok)            
        self.process_named_options(tok)

        boxes, pool_info, is_azure_pool, is_azure_box = box_information.get_box_list(self.core)
        #print("boxes=", boxes, ", is_azure_pool=", is_azure_pool)

        if target_controller:
            self.client.kill_controller_by_boxes(boxes)
        else:
            # run names take priority 
            if run_names:
                #print("run_names=", run_names)
                # run name specified: ignore any specified pool/box/job options
                runs_by_box = self.core.get_runs_by_box(run_names)
                kill_results_by_boxes = self.core.kill_runs_by_boxes(runs_by_box)
                self.print_kill_results(kill_results_by_boxes)
            else:
                # target all runs (filtered by pool/box/job)    
                job_id = self.config.get("general", "job")
                if job_id:
                    # kill all runs for job
                    kill_results_by_boxes = self.core.kill_runs_by_job(job_id)
                    self.print_kill_results(kill_results_by_boxes, "\njob {} terminated:".format(job_id))
                else:
                    # kill all runs for pool/boxes
                    runs_by_box = {box:"all" for box in boxes}  
                    kill_results_by_boxes = self.core.kill_runs_by_boxes(runs_by_box)
                    self.print_kill_results(kill_results_by_boxes)

    def print_kill_results(self, kill_results_by_boxes, run_summary=None):
        #print("kill_results_by_boxes=", kill_results_by_boxes)

        if run_summary:
            print(run_summary)

        for box_name, results in kill_results_by_boxes.items():

            # show box name as upper to emphasize where kill happened
            box_name = box_name.upper()

            if not run_summary:
                print("box {}:".format(box_name))

            if not results:
                print("  no jobs running/queued")
            else:
                for result in results:
                    if not result:
                        continue

                    #print("result=", result)
                    ws_name = result["workspace"]
                    run_name = result["run_name"]
                    killed = result["killed"]
                    status = result["status"]
                        
                    full_name = ws_name + "/" + run_name

                    if killed:
                        if status == "cancelled":
                            print("  {} removed from queue".format(full_name))
                        else:
                            print("  {} killed".format(full_name))
                    else:
                        print("  {} has already exited, status={}".format(full_name, status))

    def get_info_for_run(self, ws, run_name):
        cmdline = None
        box_name = None
        parent_name = None
        node_index = None

        records = self.store.get_run_log(ws, run_name)

        # get cmdline
        for record in records:
            if record["event"] == "cmd":
                dd = record["data"]
                cmdline = dd["cmd"]
                break

        for record in records:
            if record["event"] == "created":
                dd = record["data"]
                box_name = dd["box_name"]
                node_index = dd["node_index"]
                # looks like we no longer log the parent name
                #parent_name = dd["parent_name"]
                parent_name = run_name.split(".")[0] if "." in run_name else None
                break

        return cmdline, box_name, parent_name, node_index

    def parse_rerun_cmd(self, tok):
        run_name = self.scanner.scan()     # skip over "log" keyword
        if not run_name:
            utils.user_error("must specify a run name")

        tok = self.scanner.scan()

        # process any in-line options for this command            
        self.process_named_options(tok)

        # NOTE: validate_run_name() call must be AFTER we call process_named_options()
        ws, run_name, full_run_name = utils.validate_run_name(self.store, self.ws, run_name)

        # extract "prompt" and "args" from cmdline
        cmdline, box_name, parent_name, node_index = \
            self.get_info_for_run(self.ws, run_name)

        #print("cmdline=", cmdline)

        prompt = "  xt "
        args = ""
        found_py = False
        for part in cmdline:
            if found_py:
                args += part + " "
            else:
                prompt += part + " "
                if part.endswith(".py"):
                    found_py = True

        print("edit/accept command-line arguments for {}".format(full_run_name))
        args = utils.input_with_default(prompt, args)

        # start with support for simple case (NO POOL, NO --repeat, NO hyperparameter)
        box_cmd_parts = (prompt[5:] + args).strip().split(" ")
        #print("box_cmd_parts=", box_cmd_parts)

        job_id = self.store.create_job()

        # full_run_name = self.ws + "/" + run_name
        # runs_by_box = {"box_name": full_run_name}
        # self.store.log_job_info(job_id, pool, runs_by_box)

        # # run the job
        # run_data = {"run_name": run_name, "cmd_parts": box_cmd_parts, "box_name": box_name}
      
        #self.client.run_job(job_id, [run_data], boxes=[box_name], pool_info={}, is_azure_batch_job=False)
        using_hp = False
        resume_name = None
        keep_name = False
        demand_mode = False
        cmds_by_node = {"node0": box_cmd_parts}
        sweep_text = None

        run_data_list_by_box = self.core.run_request(box_cmd_parts, using_hp, resume_name, keep_name, demand_mode, 
            cmds_by_node, sweep_text)

        self.attach_if_needed(run_data_list_by_box)


    def parse_python_or_run_cmd(self, tok, is_docker=False):
        # tok is "python", "run", "docker", or "xxx.py"
        utils.timing("run_cmd")
        args = self.args

        arg_index = self.get_scanner_arg_index(args)
        if is_docker:
            # skip back to "docker"
            arg_index -= 1
        elif self.match(tok, "run"):
            # skip over "run" 
            arg_index += 1     

        cmd_parts = args[arg_index:]
        # remove any funny space-only cmd parts
        cmd_parts = [cp for cp in cmd_parts if cp]
        #print("cmd_parts=", cmd_parts)

        if tok.endswith(".py"):
            target_file = tok
        else:
            target_file = self.core.get_target(cmd_parts)
            
        if not target_file:
            utils.user_error("command has not target file")

        if not is_docker and not os.path.exists(target_file):
            utils.user_error("target file not found: {}".format(target_file))

        if tok.endswith(".py"):
            cmd_parts.insert(0, "python")
            cmd_parts.insert(1, "-u")
        if self.match(tok, "python"):
            # add flag for unbuffered output to keep console output looking normal
            cmd_parts.insert(1, "-u")

        # advance the scanner to end to avoid ('extra input' errors)
        while tok:
            tok = self.scanner.scan()

        boxes, pool_info, is_auzre_pool, is_azure_box = box_information.get_box_list(self.core)
        num_boxes = len(boxes)

        # build a list of arg_set's for each hyperparam run
        # if no hyperparams are detected, we just return a single arg_set
        max_gen = self.config.get("general", "runs")
        dry_run = self.config.get("general", "dry-run")
        search_type = self.config.get("hp-search", "search-type")
        hparams = HPProcess()

        # gather/process cmd line hyperparameters
        using_hp, arg_sets, template_parts, sweep_text = \
            hparams.generate_hparam_args(cmd_parts, max_gen=max_gen, search_type=search_type)

        #print("after hp processing, using_hp=", using_hp)

        if using_hp:
            # distribute runs over boxes in pool
            #print("arg_sets=", arg_sets)

            total_child_runs = len(arg_sets)
            # build cmd-list form of sweeps file
            cmds_by_node = {}
            node_index = 0

            # build cmd_parts and distribute them among nodes
            for arg_set in arg_sets:
                child_cmd_parts = hparams.fill_in_template(template_parts, arg_set)
                node_id = "node" + str(node_index)

                if not node_id in cmds_by_node:
                    cmds_by_node[node_id] = []
                cmds_by_node[node_id].append(child_cmd_parts)
                node_index += 1

                if node_index >= num_boxes:
                    node_index = 0

            # cmd_parts will be read from sweeps-list file as each child is spawned

            # preserve original cmd_parts (needed downstream, but won't really be used)
            #cmd_parts = []

            if True:   # dry_run:
                # print cmds by node
                for node_id, cmds in cmds_by_node.items():
                    if dry_run:
                        print("DRY RUN - runs for {}:".format(node_id))
                    else: 
                        print("runs for {}:".format(node_id))
                    for cmd_parts in cmds:
                        print("  cmd_parts=", cmd_parts)
                if dry_run:
                    return
        else:
            cmds_by_node = None

        demand_mode = self.config.get("general", "demand-mode")
        resume_name = self.config.get("general", "resume")
        keep_name = self.config.get("general", "keep-name")

        #print("before run_request: cmd_parts=", cmd_parts)

        run_data_list_by_box = self.core.run_request(cmd_parts, using_hp, resume_name, keep_name, demand_mode, 
            cmds_by_node, sweep_text)

        self.attach_if_needed(run_data_list_by_box)

    def attach_if_needed(self, run_data_list_by_box):
        # ATTACH or provide attach cmd
        first_run = run_data_list_by_box[0][0]   
        attach = self.config.get("general", "attach")

        if attach:
            time.sleep(1)
            self.client.monitor_attach_run(self.ws, first_run["run_name"], show_waiting_msg=False)
        else:
            box_name = first_run["box_name"]
            full_run_name = self.ws + "/" + first_run["run_name"].upper()   
            print(f"To view output: xt attach {full_run_name}")

    def parse_attach_cmd(self):
        run_name = self.scanner.scan()   # skip over "attach"
        tok = self.scanner.scan()        # skip over the run name

        # process any in-line options for this command            
        self.process_named_options(tok)

        # NOTE: validate_run_name() call must be AFTER we call process_named_options()
        ws, run_name, full_run_name = utils.validate_run_name(self.store, self.ws, run_name)

        self.client.monitor_attach_run(ws, run_name)

    def parse_status_cmd(self):
        tok = self.scanner.scan()   # skip over the "status"
        ws, run_name, full_run_name = None, None, None
        validate_run = False

        if tok and not self.is_option(tok):
            run_name = tok
            tok = self.scanner.scan()          # skip over run_name
            validate_run = True

        # process any in-line options for this command            
        self.process_named_options(tok)

        if validate_run:
            # NOTE: validate_run_name() call must be AFTER we call process_named_options()
            ws, run_name, full_run_name = utils.validate_run_name(self.store, self.ws, run_name)

        active = self.config.get("general", "active")
        queued = self.config.get("general", "queued")
        monitor = self.config.get("general", "monitor")
        auto_start = self.config.get("general", "auto-start")

        boxes, pool_info, is_azure_pool, is_azure_box  = box_information.get_box_list(self.core)

        def monitor_work():
            # BOX LOOP
            text = ""
            for b, box_name in enumerate(boxes):
                # make everyone think box_name is our current controller 
                self.client.change_box(box_name, auto_start)

                box_addr = box_information.get_box_addr(self.config, box_name)
                if not self.client.is_controller_running(box_addr, utils.CONTROLLER_PORT):
                    text += "box: " + box_name + "\n"
                    text += "  controller is NOT running\n"
                else:
                    self.client.change_box(box_name, False)

                    text += self.get_core_status() + "\n"
                    text += self.get_box_status() + "\n"

                    text +=  "\n" + "runs on " + box_name.upper() + ":\n"
                    text += self.client.jobs_report(ws=ws, run_name=run_name)

            return text

        # MONITOR-ENABLED COMMAND
        self.client.monitor_loop(monitor, monitor_work)

    def get_core_status(self):
       text = "\nstore: " + self.store_type.upper() + ", workspace: " + self.ws.upper() + ", box: " + \
            self.box.upper()
       return text
        
    def get_box_status(self, indent=""):
        elapsed = self.client.get_controller_elapsed()
        elapsed = str(datetime.timedelta(seconds=elapsed))
        elapsed = elapsed.split(".")[0]   # get rid of decimal digits at end

        xt_version = self.client.get_controller_xt_version()

        cname = "localhost" if self.box=="local" else self.box
        max_runs = self.client.get_controller_max_runs()
        ip_addr = self.client.get_controller_ip_addr()
 
        text = indent + "{} controller (xt {}, addr: {}, running time: {}, max-runs: {})".format(
            cname.upper(), xt_version, ip_addr, elapsed, max_runs)
        return text

    def parse_keygen_cmd(self):
        tok = self.scanner.scan()     # skip over "keygen"

        # process any in-line options for this command            
        self.process_named_options(tok)

        overwrite = self.config.get("general", "overwrite")
        status = self.core.keygen(overwrite)
        if status:
            print("key pair successfully generated.")

    def parse_keysend_cmd(self):
        # syntax: xt keysend <box name> 
        box_name = self.scanner.scan()     # skip over "keysend"
        if not box_name:
            utils.user_error("must specify a box name/address")
        tok = self.scanner.scan()     # skip over box_name

        # process any in-line options for this command            
        self.process_named_options(tok)

        box_addr = box_information.get_box_addr(self.config, box_name)
        if utils.is_localhost(box_name, box_addr) or box_name == "azure-batch":
            utils.user_error("must specify a remote box name or address (e.g., xt keysend johnsmith@104.211.38.123")

        print("this will require 2 connections to the remote host, so you will be prompted for a password twice")
        status = self.core.keysend(box_name)
        if status:
            print("public key successfully sent.")

    def parse_ssh_cmd(self):
        # syntax: xt ssh <box name> [ <cmds> ]
        box_name = self.scanner.scan()     # skip over "ssh"
        if not box_name:
            utils.user_error("must specify a box name/address")

        cmd = self.scanner.get_rest_of_text()
        box_addr = box_information.get_box_addr(self.config, box_name)
        capture_output = True if cmd else False
        #print("ssh_cmd: box=", box_addr, ", cmd=", cmd)

        exit_code, output = utils.sync_run_ssh(self, box_addr, cmd, capture_output=capture_output)
        if capture_output:
            print(output)

    def is_valid_exper_name(self, name):
        # no restrictions for now   
        return True

    def to_int(self, text):
        try:
            value = int(text)
        except:
            value = None
        return value

    def parse_workspace_cmd(self):
        tok = self.scanner.scan()     # skip over "workspace"
        #value, tok = self.parse_optional_value(tok)

        # process any in-line options for this command            
        self.process_named_options(tok)

        report = True
        # if value:
        #     self.scanner.scan()     # skip over value
        #     # if not self.store.does_workspace_exist(value):
        #     #     utils.user_error("workspace does not exist: " + value)
        #     #     report = False
        #     # else:
        #     self.config.set("general", "workspace", value=value)
        #     #self.save_user_settings()

        if report:
            ws = self.config.get("general", "workspace")
            print("default workspace: " + ws)

    def parse_max_runs_cmd(self):
        tok = self.scanner.scan()     # skip over "max-runs"
        #value, tok = self.parse_optional_value(tok)

        # if value:
        #     value = self.to_int(value)
        #     if value is None:
        #         utils.user_error("max-runs must be a integer, but got value={} ".format(value))

        # process any in-line options for this command            
        self.process_named_options(tok)

        def pool_work(box_name, box_index):
            # if value:
            #     #print("value=", value, ", type(value)=", type(value))
            #     self.config.set("boxes", box_name, dict_key="max-runs", value=value, suppress_warning=True)
            #     #self.save_user_settings()
            #     self.client.set_controller_max_runs(value)

            text = self.get_box_status()
            print(text)

        boxes, pool_info, is_azure_pool, is_azure_box  = box_information.get_box_list(self.core)
        self.client.pool_loop(boxes, pool_work, True)

    def parse_optional_value(self, tok):
        value = None
        if (tok == "="):
            value = self.scanner.scan()     # skip over optional "="
            tok = self.scanner.scan()     # skip over value
        elif tok and not self.is_option(tok):
            value = tok
            tok = self.scanner.scan()     # skip over value

        return value, tok

    # def parse_diagnostics_cmd(self):
    #     tok = self.scanner.scan()     # skip over "diagnostics"
    #     value, tok = self.parse_optional_value(tok)

    #     # process any in-line options for this command            
    #     self.process_named_options(tok)

    #     report = True
    #     if value:
    #         value = value.lower() in ["1", "true", "on"]

    #         #print("value=", value, ", type(value)=", type(value))
    #         self.config.set("general", "diagnostics", value=value)
    #         #self.save_user_settings()

    #     if report:
    #         print("diagnostics: " + str(self.config.get("general", "diagnostics")))

    def parse_restart_cmd(self):
        tok = self.scanner.scan()     # skip over "restart"
        if not self.match(tok, "controller"):
            utils.user_error("restart command expected keyword 'controller'")

        tok = self.scanner.scan()     # skip over controller
        visible = self.match(tok, "visible")

        if visible:
            tok = self.scanner.scan()         # skip over visible

        # process any in-line options for this command            
        self.process_named_options(tok) 

        demand_mode = self.config.get("general", "demand-mode")

        def pool_work(box_name, box_index):
            self.client.restart_controller(box_name=box_name, visible=visible, demand_mode=demand_mode)
            print("{} controller restarted".format(box_name))

        boxes, pool_info, is_azure_pool, is_azure_box  = box_information.get_box_list(self.core)
        self.client.pool_loop(boxes, pool_work, False)

    def parse_test_cmd(self):
        '''
        This command is used for internal XT testing only.
        '''
        value = self.scanner.scan()     # skip over "test"

        tok = self.scanner.scan()       # skip over value

        # process any in-line options for this command            
        self.process_named_options(tok)

        desc = self.config.get("general", "description")
        print("desc=", desc)

        #self.job_from_run(value)
        #self.test_job_api()
        #self.test_azure_batch()
        #self.test_azure_box()
        #self.test_job_info(value)

    def parse_addr_cmd(self):
        box_name = self.scanner.scan()     # skip over "addr"
        tok = self.scanner.scan()   # skip over box_name

        # process any in-line options for this command            
        self.process_named_options(tok)

        box_addr = box_information.get_box_addr(self.config, box_name)
        print("{} address: {}".format(box_name, box_addr))

    def parse_upload_cmd(self):
        # syntax: upload [file] [from] <local path> [to] <file share path>
        tok = self.scanner.scan()     # skip over UPLOAD
    
        #print("first tok after UPLOAD: ", tok)
        if self.match(tok, ["file"]):
            tok = self.scanner.scan()     # skip over optional FILES

        if self.match(tok, ["from"]):
            tok = self.scanner.scan()     # skip over optional FROM

        local_path = tok
        tok = self.scanner.scan()     # skip over LOCAL PATH

        if not local_path:
            utils.user_error("must supply a LOCAL file path")
        print("local_path=", local_path)

        if self.match(tok, ["to"]):
            tok = self.scanner.scan()     # skip over optional TO

        store_path = tok
        tok = self.scanner.scan()     # skip over STORE PATH

        if not store_path:
            utils.user_error("must supply a STORE file path")
        print("store_path=", store_path)

        # process any in-line options for this command            
        self.process_named_options(tok)

        exper_name = self.config.get("general", "experiment")
        job_name = self.config.get("general", "job")

        if job_name:
            jf = self.store.job_files(job_name, use_blobs=False)
            jf.upload_file(store_path, local_path)
            print("file uploaded to JOB share: " + job_name)
        elif exper_name:
            ef = self.store.experiment_files(self.ws, exper_name, use_blobs=False)
            ef.upload_file(store_path, local_path)
            print("file uploaded to EXPERIMENT share: " + exper_name)
        else:
            wf = self.store.workspace_files(self.ws, use_blobs=False)
            wf.upload_file(store_path, local_path)
            print("file uploaded to WORKSPACE share: " + self.ws)

    def parse_download_cmd(self):
        # syntax: download [file] [from] <file share path> [to] <local path>
        tok = self.scanner.scan()     # skip over DOWNLOAD
    
        #print("first tok after DOWNLOAD: ", tok)
        if self.match(tok, ["file"]):
            tok = self.scanner.scan()     # skip over optional FILES

        if self.match(tok, ["from"]):
            tok = self.scanner.scan()     # skip over optional FROM

        store_path = tok
        tok = self.scanner.scan()     # skip over LOCAL PATH

        if not store_path:
            utils.user_error("must supply a STORE file path")
        print("store_path=", store_path)

        if self.match(tok, ["to"]):
            tok = self.scanner.scan()     # skip over optional TO

        local_path = tok
        tok = self.scanner.scan()     # skip over STORE PATH

        if not local_path:
            utils.user_error("must supply a LOCAL file path")
        print("local_path=", local_path)

        # process any in-line options for this command            
        self.process_named_options(tok)

        exper_name = self.config.get("general", "experiment")
        job_name = self.config.get("general", "job")

        if job_name:
            jf = self.store.job_files(job_name, use_blobs=False)
            jf.download_file(store_path, local_path)
            print("file downloaded from JOB share: " + job_name)
        elif exper_name:
            ef = self.store.experiment_files(self.ws, exper_name, use_blobs=False)
            ef.download_file(store_path, local_path)
            print("file downloaded from EXPERIMENT share: " + exper_name)
        else:
            wf = self.store.workspace_files(self.ws, use_blobs=False)
            wf.download_file(store_path, local_path)
            print("file downloaded from WORKSPACE share: " + self.ws)

    def parse_delete_file_cmd(self, tok):
        # syntax: delete file [from] <file share path> 
        tok = self.scanner.scan()     # skip over FILE
    
        if self.match(tok, ["from"]):
            tok = self.scanner.scan()     # skip over optional FROM

        store_path = tok
        tok = self.scanner.scan()     # skip over LOCAL PATH

        if not store_path:
            utils.user_error("must supply a STORE file path")
        print("store_path=", store_path)

        # process any in-line options for this command            
        self.process_named_options(tok)

        exper_name = self.config.get("general", "experiment")
        job_name = self.config.get("general", "job")

        if job_name:
            jf = self.store.job_files(job_name, use_blobs=False)
            jf.delete_files(store_path)
            print("file deleted from JOB share: " + job_name)
        elif exper_name:
            ef = self.store.experiment_files(self.ws, exper_name, use_blobs=False)
            ef.delete_files(store_path)
            print("file deleted from EXPERIMENT share: " + exper_name)
        else:
            wf = self.store.workspace_files(self.ws, use_blobs=False)
            wf.delete_files(store_path)
            print("file deleted from WORKSPACE share: " + self.ws)

    def parse_list_files_cmd(self):
        # syntax: list files <file share path> 
        tok = self.scanner.scan()     # skip over LIST FILES
        
        store_path = tok
        tok = self.scanner.scan()     # skip over LOCAL PATH

        # if not store_path:
        #     store_path = "."
        #print("store_path=", store_path)

        # process any in-line options for this command            
        self.process_named_options(tok)

        exper_name = self.config.get("general", "experiment")
        job_name = self.config.get("general", "job")

        if job_name:
            jf = self.store.job_files(job_name, use_blobs=False)
            dirs, files = jf.get_filenames(store_path)
        elif exper_name:
            ef = self.store.experiment_files(self.ws, exper_name, use_blobs=False)
            dirs, files = ef.get_filenames(store_path)
        else:
            wf = self.store.workspace_files(self.ws, use_blobs=False)
            dirs, files = wf.get_filenames(store_path)

        print("files:")
        if dirs:
            for dir in dirs:
                print("  {} (dir)".format(dir))

        if files:
            for file in files:
                print("  {}".format(file))

    def parse_explore_cmd(self):
        dest_name = self.scanner.scan()     # skip over "explore" keyword
        if not dest_name:
            utils.user_error("hx command must specify the job or experiment name")
        tok = self.scanner.scan()            # skip over dest_name

        # process any in-line options for this command            
        self.process_named_options(tok)

        #utils.start_async_run_detached("python ")
        hx_metric = self.config.get("hp-search", "hx-metric")
        score_rollup = self.config.get("metrics", hx_metric, default_value="last")
        cache_dir = self.config.get("hp-search", "hx-cache-dir")

        # we need to respond to the job or experiment name user has specified
        aggregate_dest = "job" if dest_name.startswith("job") else "experiment"

        #print("hx_metric=", hx_metric)
        if aggregate_dest == "job":
            filenames = self.store.get_job_filenames(dest_name, utils.HP_CONFIG_DIR)
            if not filenames:
                utils.user_error("Missing hp-config file for job={}".format(dest_name))
        else:
            filenames = self.store.get_experiment_filenames(self.ws, dest_name, utils.HP_CONFIG_DIR)
            if not filenames:
                utils.user_error("Missing hp-config file for experiment={}".format(dest_name))

        fn_hp_config = filenames[0]
        print("found hp-config file: ", fn_hp_config)

        hx = HyperparameterExplorer(self.ws, hx_metric, score_rollup, cache_dir, aggregate_dest, dest_name, fn_hp_config)
        hx.run()

    def is_controller_cmd(self, cmd):
        ''' returns True if the specified command relies on the controller running'''
        uses_controller = True

        # note: the pool/run/python/attach cmds do their own controller initialization (with support for pools), so it returns False here
        match = self.match(cmd, ["keygen", "keysend", "ssh", "ws", "workspace", "experiment", "box", "address", "restart", "kill", 
                "list", "max-runs", "test", "status", "run", "python", "docker", "attach", "diagnostics", "view"])
        if match or cmd.endswith(".py"):
            uses_controller = False

            # exception is "kill" for non-controller targets
            if self.match(match, "kill") and not self.match(self.scanner.peek(), "controller"):
                uses_controller = True

        utils.diag("  cmd={}, uses_controller={}".format(cmd, uses_controller))
        return uses_controller

    def is_default_ws_cmd(self, cmd):
        ''' returns True if the specified command depends on the default workspace'''
        needs_ws = False
        run_cmds = ["python", "run", "docker", "list", "extract", "attach", "delete", "copy", "rerun"]
        match = self.match(cmd, run_cmds)

        if match:
            needs_ws = True
            if match in ["list", "delete"] and self.match(self.scanner.peek(), ["workspace", "file"]):
                needs_ws = False
        elif cmd.endswith(".py"):
            needs_ws = True

        return needs_ws

    def preprocess_cmd(self, cmd):
        # here the commands for which we do NOT want to call init_controller:
        #  keygen, keysend, kill controller, restart controller
        if self.box == "local":
            self.box = utils.get_hostname()

        utils.diag("initializing")
        init_client = True
        init_controller = self.is_controller_cmd(cmd)

        # init the local/remote CONTROLLER
        if init_client:
            try:
                self.init_client_and_store()
                utils.diag("  client and store initialized")
            except BaseException as ex:
                utils.report_exception(ex, "client/store initialization")

            # don't init the controller if this is the RESTART CONTROLLER or KILL CONTROLLER command
            if init_controller:
                try:
                    self.client.init_controller(self.box)
                    utils.diag("  controller initialized")
                except BaseException as ex:
                    #raise ex   # uncomment to see the stack trace
                    utils.report_exception(ex, "controller initialization")

        need_default_ws = self.is_default_ws_cmd(cmd)
        if need_default_ws:
            # must be non-empty
            if not self.ws:
                utils.user_error("this command requires a workspace; please use 'xt workspace <name>' to set")

            # must be a legal ws name
            if not self.store.is_legal_workspace_name(self.ws):
                utils.user_error("the default/specified workspace name is not legal for the STORE: " + str(self.ws))

            # must exist
            if not self.store.does_workspace_exist(self.ws):
                #print("this command requires a workspace")
                print("the specified/default workspace does not exist: " + self.ws)
                answer = input("OK to create?  (y/n) [y]: ")
                if answer in ["", "y"]:
                    self.store.create_workspace(self.ws)
                else:
                    utils.user_exit("command cancelled")

    def parse_commands(self, cmd):
        self.preprocess_cmd(cmd)
        
        if self.match(cmd, "config"):
            self.parse_config_cmd()
        elif self.match(cmd, "list"):
            self.parse_list_commands()
        elif self.match(cmd, ["view", "show"]):
            self.parse_view_commands()
        elif self.match(cmd, "plot"):
            self.parse_plot_command()
        elif self.match(cmd, "create"):
            self.parse_create_commands()
        elif self.match(cmd, "delete"):
            self.parse_delete_commands()
        elif self.match(cmd, "docker"):
            self.parse_docker_commands()
        elif self.match(cmd, ["python", "run"]) or cmd.endswith(".py"):
            cmd = self.parse_python_or_run_cmd(cmd)
        elif self.match(cmd, ["rerun", "re-run"]):
            cmd = self.parse_rerun_cmd(cmd)
        elif self.match(cmd, "extract"):
            cmd = self.parse_extract_cmd()  
        elif self.match(cmd, "dir"):
            cmd = self.parse_dir_cmd()  
        elif self.match(cmd, "cat"):
            cmd = self.parse_cat_cmd()  
        elif self.match(cmd, "attach"):
            cmd = self.parse_attach_cmd()
        elif self.match(cmd, "status"):
            cmd = self.parse_status_cmd()
        elif self.match(cmd, "kill"):
            cmd = self.parse_kill_cmd()
        elif self.match(cmd, "keygen"):
            self.parse_keygen_cmd()
        elif self.match(cmd, "keysend"):
            self.parse_keysend_cmd()
        elif self.match(cmd, "ssh"):
            self.parse_ssh_cmd()
        elif self.match(cmd, "test"):
            self.parse_test_cmd()
        elif self.match(cmd, ["ws", "workspace"]):
            self.parse_workspace_cmd()
        elif self.match(cmd, "max-runs"):
            self.parse_max_runs_cmd()
        elif self.match(cmd, "restart"):
            self.parse_restart_cmd()
        elif self.match(cmd, "address"):
            self.parse_addr_cmd()
        elif self.match(cmd, "explore"):
            self.parse_explore_cmd()
        elif self.match(cmd, "upload"):
            self.parse_upload_cmd()
        elif self.match(cmd, "download"):
            self.parse_download_cmd()
        else:
            utils.user_error(f"unrecognized start of command: {cmd}")

        if self.scanner.token != None:
            utils.user_error("unexpected text at end of command: " + self.scanner.token)

    def validate_storage_config_entries(self):
        username = self.config.get("core", "username")
        store_name = self.config.get("azure", "storage-name")
        store_key = self.config.get("azure", "storage-key")

        if not username:
            utils.user_error("'username' must be set in [core] section of XT config file")

        if not store_name or store_name.startswith("xxxx"):
            utils.user_error("'storage-name' must be set in [azure] section of XT config file")

        if not store_key or store_key.startswith("xxxx"):
            utils.user_error("'storage-key' must be set in [azure] section of XT config file")

    def _init_store(self):
        # if self.config is None:
        #     self.config = read_config()

        self.validate_storage_config_entries()

        self.ws = self.config.get("general", "workspace")
        #print("self.ws=", self.ws)

        store_type = self.config.get("core", "store-type")
        run_cache_dir = self.config.get("general", "run-cache-dir")
        tqdm_enabled = self.config.get("general", "tqdm-enabled")
        #print("tqdm_enabled=", tqdm_enabled)

        if store_type == "file-store":
            # init file-based STORE 
            store_root = utils.expand_vars(self.config.get("core", "file-store-path"))
            #print("initializing FILE STORE: ", fn)
            
            self.store = Store(store_root, run_cache_dir=run_cache_dir, tqdm_enabled=tqdm_enabled)
        elif store_type == "azure-store":
            # init AZURE-based STORE
            #print("initializing AZURE BLOB STORE: ", self.config.storage_name)
            store_name = self.config.get("azure", "storage-name")
            store_key = self.config.get("azure", "storage-key")
 
            self.store = Store(store_name, store_key, run_cache_dir=run_cache_dir, tqdm_enabled=tqdm_enabled)
        # elif store_type == "aml":
        #     # init AML-based STORE
        #     #print("initializing AZURE AML STORE: ", self.config.subscription_id)
        #     subscription_id = self.config.get("azure", "subscription-id")
        #     resource_group = self.config.get("azure", "resource-group")
        #     location = self.config.get("azure", "location")
        #     self.store = Store(subscription_id=subscription_id, resource_group=resource_group, location=location)
        else:
            raise Exception("unsupported store value: ", store)

        # ensure the default workspace exists
        # if not self.ws:
        #     raise Exception("default workspace not set; use 'xt workspace <value>' to fix")

        # if not self.store.does_workspace_exist(self.ws):
        #     self.store.create_workspace(self.ws)

        return self.config

    def init_client_and_store(self):
        self._init_store()

        self.client = Client(self.config, self.store)
        self.client.started = self.started

        self.core = CmdCore(self.config, self.store, self.client, self.explicit_options)
        self.client.core = self.core
        #print("self.client.core=", self.client.core)

    def print_cmd_help(self):
        utils.enable_ansi_escape_chars_on_windows_10()
        text = help.get_cmd_help()
        help.color_print_lines(text)

    def parse_cmdline_args(self):
        # first, handle commands that do not require XTClient 
        self.verb = "start" if sys.platform == "win32" else "open"

        tok = self.scanner.token
        #print("first command tok=", tok)
        
        is_help = self.match(tok, "help")
        if is_help or self.config.get("general", "help"):
            if is_help:
                tok = self.scanner.scan()

            if not tok or self.match(tok, "about"):
                text = help.get_about_help()
                print(text)
            elif self.match(tok, "api"):
                text = help.get_api_help()
                print(text)
            elif self.match(tok, ["cmds", "commands"]):
                self.print_cmd_help()
            else:
                utils.user_error("unrecognized help argument: " + tok)
        elif self.match(tok, ["version", "build"]):
            print(utils.BUILD)
        else:
            self.parse_commands(tok)

    def parse_cmdline_options(self, args):
        self.build_default_options()

        cmd = " ".join(args)
        self.scanner = Scanner(cmd)
        tok = self.scanner.scan()
        #print("first tok=", tok)

        # parse options
        while tok and tok.startswith("--"):
            #=", tok)
            tok = self.parse_option(tok)
            #print("tok=", tok)

    def init_config_settings_and_options(self, args):
        # load normal config file
        self.config = xt_config.get_merged_config()

        # apply cmdline options
        self.parse_cmdline_options(args)

        self.on_options_changed()
        timing_enabled = self.config.get("general", "timing")
        utils.set_timing_data(self.started, timing_enabled)
        utils.timing("started")

    def on_options_changed(self):
        # now that config, settings, and options are loaded, its safe to cache
        # some settings to make the code cleaner

        if self.config:
            self.box = self.config.get("core", "box")
            if self.box == "local":
                self.box = utils.get_hostname()
                self.config.set("core", "box", value=self.box)

            self.store_type = self.config.get("core", "store-type")
            self.ws = self.config.get("general", "workspace")
            utils.diagnostics = self.config.get("general", "diagnostics")

            if self.client:
                self.client.on_options_changed()

            if self.core:
                self.core.on_options_changed(self.explicit_options)

    def run_core(self):
        error = False

        # wrap all COMMAND PROCESSING in a try/except
        try:
            cmd_args = self.args

            # handle short and long help functions before initializing the XT Client 
            if len(cmd_args) == 0:
                #text = help.get_about_help()
                text = help.get_short_help()
                print(text)
            elif cmd_args[0] == "--help":
                text = help.get_about_help()
                print(text)
            else:
                # early cmd parsing to handle "config" cmd early 
                # so that errors in the config file can be edited with "xt config"
                cmd = " ".join(cmd_args)
                self.scanner = Scanner(cmd)
                tok = self.scanner.scan()
                if tok == "config":
                    self.parse_config_cmd()
                else:
                    # start parsing commands 
                    self.init_config_settings_and_options(cmd_args)
                    self.parse_cmdline_args()
        except BaseException as ex:
            # print("run_core: printing exception...")
            print(ex)
            error = True

            # does user want a stack-trace?
            if not self.config or self.config.get("general", "raise", suppress_warning=True):
                raise ex

        return error

    def add_quotes_to_string_args(self):
        for i, arg in enumerate(self.args):

            # don't process an app's args
            # if arg in ["run", "python"]:
            #     break

            if " " in arg:  
                if arg.startswith("--"):
                    # --option=value
                    parts = arg.split("=")
                    assert(len(parts)==2)
                    arg = parts[0] + '="' + parts[1] + '"'
                else:
                    arg = '"' + arg + '"'
                self.args[i] = arg

    # def fake_download(self, callback):
    #     count = 30
    #     callback(0, 30)

    #     for i in range(count):
    #         time.sleep(.1)
    #         callback(i, count)

    def run(self, cmd=None):
        self.started = time.time() - .8   # we lose about .8 secs from xt.bat
        #utils.feedback("starting", is_first=True)

        #print("cmd=", cmd)
        #print("XT: sys.argv=", sys.argv)

        # command can be passed or taken from command line
        if cmd:
            self.args = cmd.split(" ")
        else:
            self.args = sys.argv[1:]
        
        self.add_quotes_to_string_args()
        #print("self.args=", self.args)

        # outer loop REPL mode
        if len(self.args) == 1 and self.args[0] == "repl":
            while True:
                cmd = input("xt> ")
                if not cmd:
                    continue

                if cmd in ["repl", "off", "exit", "close", "bye"]:
                    break
                elif cmd in ["cls", "clear"]:
                    #utils.enable_ansi_escape_chars_on_windows_10()
                    #print(chr(27) + "[2J")
                    os.system('cls' if os.name == 'nt' else 'clear')
                else:
                    self.args = cmd.split(" ")
                    error = self.run_core()
        else:
            error = self.run_core()

        utils.timing("exiting")
        #print("exiting with exit(0)")
        if error:
            sys.exit(1)     # signal to caller (quick-test.py) that we aborted
        else:
            sys.exit(0)     # exit cleanly, even if we caught a ctrl-C while waiting for experiment to complete
