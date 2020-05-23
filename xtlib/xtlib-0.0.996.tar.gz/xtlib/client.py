# client.py - a high level API for working with XT's STORE and CONTROL API's, leveraging the config file data.

import os
import sys
import json
import rpyc
import time
import arrow
import socket 
import socket 
import signal   
import psutil    
import datetime
import numpy as np
import subprocess
from time import sleep
import azure.storage.blob as azureblob
import azure.batch.models as batchmodels

from .helpers.bag import Bag
from .helpers.key_press_checker import KeyPressChecker

from . import utils as utils 
from .store import Store
from .azure_batch import AzureBatch
from .list_builder import ListBuilder   
from . import box_information
from . import app_information

# constants
SH_NAME ="xtc_run.sh"

CONTROLLER_NAME_PATTERN = "xtlib.controller"
DETACHED_PROCESS = 0x00000008
CREATE_NO_WINDOW = 0x08000000

class Client():
    '''This class has about 30 functions that implement the features of the XT cmdline app.
    '''
    def __init__(self, config=None, store=None, core=None):
        self.config = config
        self.store = store
        self.blob_client = None     # will allocate on demand
        self.visible_for_debugging = False
        self.port = utils.CONTROLLER_PORT
        self.conn = None
        self.core = core
        #print("core=", core)

        self.on_options_changed()

    def create_new_client(self, config):
        return Client(config, self.store, self.core)

    def on_options_changed(self):
        self.box = self.config.get("core", "box")
        self.ws = self.config.get("general", "workspace")
        utils.diagnostics = self.config.get("general", "diagnostics")

    def diag(self, msg):
        if utils.diagnostics:
            print(msg)

    def get_config(self):
        return self.config

    def kill_runs(self, run_names):
        # send results as json text so that we are not tied to controller (which may be killed immediately after this call)
        results_json_text = self.conn.root.kill_run(run_names)
        results = json.loads(results_json_text)
        return results

    def is_controller_running(self, box_addr, port):
        # KISS: just try to connect
        is_running = False

        try:
            ip_addr = self.core.get_ip_addr_from_box_addr(box_addr)
            utils.diag("  trying to connect with: ip_addr={}, port={}".format(ip_addr, port))

            self.conn = rpyc.connect(ip_addr, port=port, config = {"allow_public_attrs" : True})
            is_running = True
        except BaseException as ex:
            utils.diag("  received exception: " + str(ex))
            is_running = False
            #raise ex   # uncomment to see the stack trace

        utils.diag("  is_controller_running: " + str(is_running))
        return is_running

    def restart_controller(self, box_name, visible=False, demand_mode=False):
        box_addr = box_information.get_box_addr(self.config, box_name)
        port = utils.CONTROLLER_PORT

        if self.is_controller_running(box_addr, port):
            self.kill_controller(box_name)

        utils.diag("  starting controller")
        if demand_mode:
            # used to test azure-batch mode of running the controller, including:
            # initialization, context file processing, shut-down, and preemption kill/restart.

            tmp_dir = utils.make_tmp_dir("restart-demand", True)
            fn_context = tmpdir + "/" + utils.FN_MULTI_RUN
            fn_context = utils.fix_slashes(fn_context, force_linux=True)
            hold_open = self.config.get("general", "hold")

            # this command runs the xt controller with a list of runs, described by the filename in fn_context
            xtc_command = "from xtlib.controller import run as run; run({}, {}, '{}', {}, {})" \
                .format(1, None, fn_context, hold_open, utils.CONTROLLER_PORT)  

            # run controller with context file
            self.init_controller(box_name, visible, demand_script=xtc_command)
        else:
            self.init_controller(self.box, visible)
        

    def kill_controller(self, box_name):
        print("kill_controller: checking running processes on: " + box_name)

        is_local = utils.is_localhost(box_name)
        #print("box_name=", box_name, ", is_local=", is_local)

        ''' kill the controller process on the specified local/remote box'''
        if is_local:  # utils.is_localhost(box_name, box_addr):
            # LOCALHOST: check if controller is running 
            python_name = "python.exe" if utils.is_windows() else "python"

            processes = psutil.process_iter()
            pythons = [p for p in processes if p.name().lower() == python_name]
            #print("pythons=", [p.cmdline() for p in pythons])

            # find the python app with our target source file name
            targets = [pp for pp in pythons if CONTROLLER_NAME_PATTERN in " ".join(pp.cmdline())]
            if targets:
                process = targets[0]

                try:
                    process.kill()
                except BaseException as ex:
                    pass

                print(" controller process={} killed".format(process.pid))
            else:
                print("controller not running")
                return False
        else:
            # REMOTE BOX: check if controller is running 
            box_addr = self.config.get("boxes", box_name, dict_key="address")
            if not box_addr:
                utils.user_error("missing address property for box: {}".format(self.box))
        
            # run PS on box to determine if controller is running
            box_cmd = "ps aux | grep controller"
            exit_code, output = utils.sync_run_ssh(self, box_addr, box_cmd)
            
            #print("result=\n", output)
            targets = [text for text in output.split("\n") if "python" in text]
            #print("targets=", targets)
            if targets:
                parts = targets[0].split(" ")

                # remove empty strings
                parts = list(filter(None, parts))

                #print("parts=", parts)
                if len(parts) > 1:
                    pid = parts[1].strip()

                    # send "kill" command to remote linux box
                    box_cmd = 'kill -kill {}'.format(pid)
                    utils.sync_run_ssh(self, box_addr, box_cmd)
            else:
                utils.diag("  controller not running")
                return False

        # note: we killed the parent process (the script that runs the xt controller), but the child 
        # process may still be running at this point and cause confusing when we do "is_controller_running()" test.
        # to work around detailed timing issues, we sleep for 3 seconds here (only slows down kill/restart commands).
        time.sleep(3)   
        return True

    def get_controller_elapsed(self):
        return self.conn.root.elapsed_time()

    def get_controller_xt_version(self):
        return self.conn.root.xt_version()

    def get_controller_log(self):
        return self.conn.root.controller_log()

    def get_controller_ip_addr(self):
        return self.conn.root.get_ip_addr()

    def get_controller_max_runs(self):
        return self.conn.root.get_max_runs()

    def set_controller_max_runs(self, value):
        #print("value=", value, ", type(value)=", type(value))
        self.conn.root.set_max_runs(value)

    def start_console_app(self, cmd, working_dir, fn_stdout, fn_stderr, console_type):
        '''
        This is the one that works for all 3 console_type values!  
        Tested on windows, 4/15/2019, rfernand, "agent1" home machine.
        '''
        if console_type == "integrated":
            hidden, detached = False, False
        elif console_type == "hidden":
            hidden, detached = True, False
        elif console_type == "visible":
            hidden, detached = True, True
        else:
            raise Exception("unsupported console_type: " + str(console_type))

        creationflags = DETACHED_PROCESS if detached else 0
        print("hidden=", hidden, ", detached=", detached)

        # apparently, we don't have to hold the file open - this is sufficient (cool!)
        if hidden:
            with open(fn_stdout, 'w') as output:
                #with open(fn_stderr, 'a') as error:
                subprocess.Popen(cmd, cwd=working_dir, creationflags=creationflags, \
                    stdout=output, stderr=subprocess.STDOUT)   # stderr=error) 
        else:
             subprocess.Popen(cmd, cwd=working_dir, creationflags=creationflags)

    def _launch_controller_localhost_windows(self, box_name, box_addr, python_script, prep_script, visible):
        fn_script_log = os.path.expanduser(utils.CONTROLLER_SCRIPT_LOG)
        fn_batch = os.path.expanduser(utils.CONTROLLER_BATCH)
        fn_controller_run_log = os.path.expanduser(utils.CONTROLLER_RUN_LOG)
        utils.ensure_dir_exists(file=fn_batch)

        python_run_cmd = 'python -u -c "{}" > {}'.format(python_script, fn_controller_run_log)
        utils.send_cmd_as_script_to_box(self, box_addr, python_run_cmd, fn_batch, prep_script, False)
        utils.diag("  running batch file: " + fn_batch)

        if visible:
            fn_batch = utils.fix_slashes(fn_batch)
            utils.diag("  running controller on LOCALHOST, Windows, fn_batch=" + str(fn_batch) + ", creationFlags=" + str(DETACHED_PROCESS))

            subprocess.Popen(fn_batch, cwd=".", creationflags=DETACHED_PROCESS) 
        else:
            with open(fn_script_log, 'w') as output:
               subprocess.Popen(fn_batch, cwd=".", creationflags=CREATE_NO_WINDOW, stdout=output, stderr=subprocess.STDOUT) 

    def _launch_controller_localhost_linux(self, box_name, box_addr, python_script, prep_script, shell_launch_prefix, visible):
        fn_script = os.path.expanduser(utils.CONTROLLER_SHELL)
        fn_controller_run_log = os.path.expanduser(utils.CONTROLLER_RUN_LOG )
        utils.ensure_dir_exists(file=fn_script)

        # nohup is most reliable when used on python (vs. the shell script)
        python_run_cmd = 'nohup python -u -c "{}" </dev/null > {} 2>&1 &'.format(python_script, fn_controller_run_log)
        utils.send_cmd_as_script_to_box(self, box_addr, python_run_cmd, fn_script, prep_script, True)

        # specify "--login" so that script can access conda, etc.
        #run_cmd = ['/bin/sh', '--login', fn_script]
        if not shell_launch_prefix:
            shell_launch_prefix = "/bin/sh --login"
        parts = shell_launch_prefix.split(" ") + [fn_script]

        # TODO: capture output here?   
        # with open(fn_script_log, 'w') as output:
        process = subprocess.Popen(parts)

    def _launch_controller_remote_linux(self, box_name, box_addr, python_script, prep_script, shell_launch_prefix, visible):
        fn_script = utils.CONTROLLER_SHELL
        fn_controller_run_log = utils.CONTROLLER_RUN_LOG

        # ensure REMOTE scripts dir exists
        box_cmd = "mkdir -p {}".format(os.path.dirname(fn_script))
        utils.sync_run_ssh(self, box_addr, box_cmd)

        # for proper bg run, we need to redirect all 3: STDIN, STDOUT, and STDERR
        # nohup python -u -c "from xtlib import controller; controller.run(max_runs=1)" </dev/null   > ~/.xt/controller.log 2>&1  &
        python_run_cmd = 'nohup python -u -c "{}" </dev/null  > {} 2>&1 &'.format(python_script, fn_controller_run_log)
        utils.send_cmd_as_script_to_box(self, box_addr, python_run_cmd, fn_script, prep_script, True)

        # the "nohup" command requires the shell
        # specify "--login" so that script can access conda, etc.
        #run_cmd = "/bin/sh --login {}".format(fn_script)
        if not shell_launch_prefix:
            shell_launch_prefix = "/bin/sh --login"
        run_cmd = shell_launch_prefix + " " + fn_script

        utils.sync_run_ssh(self, box_addr, run_cmd)

    def _launch_controller(self, box_name, box_addr, visible, demand_script=None):
        # for now, we will rely on:
        #   - the local/remote machine's active environment having xtlib installed (TODO: pip install xtlib, as needed)
        #   - remote box is running linux (TODO: support Windows-based remote boxes)

        # since we have to run multiple commands (conda and python), its much easier to develop/debug if we push
        # a shell script to the local/remote box and run that.

        box_info = box_information.BoxInfo(self.config, box_name=box_name)
        app_info = app_information.AppInfo(self.config, app_path="xtlib/controller.py", box_info=box_info)

        # app_info = self.core.get_app_info("xtlib/controller.py")
        # box_os = self.core.get_box_os(box_name)
        box_os = box_info.box_os

        # get prep script for XT controller
        #prep_script, shell_launch_prefix = self.core.get_prep_script(app_info, box_name, "combined")
        prep_script = app_info.get_prep_script("combined")
        shell_launch_prefix = box_info.shell_launch_prefix

        # this assumes we have all boxes we used defined, including "local"
        #box_info = self.core.get_box_info(box_name, {"max-runs": 1, "os": "linux"})
        max_runs = box_info.max_runs

        utils.diag("launching controller on {} (addr={}, max-runs={}, box_os={}, app={}, prep_script={})".format(
            box_name.upper(), box_addr,  max_runs, box_os, app_info.app_name, prep_script))

        if demand_script:
            python_script = demand_script
        else:
            ip_only = self.core.get_ip_addr_from_box_addr(box_addr)
            python_script = "from xtlib.controller import run as run; run(max_runs={}, my_ip_addr='{}')".format(max_runs, ip_only)

        if utils.is_localhost(box_name, box_addr):
            if utils.is_windows():
                self._launch_controller_localhost_windows(box_name, box_addr, python_script, prep_script, visible)
            else:
                self._launch_controller_localhost_linux(box_name, box_addr, python_script, prep_script, shell_launch_prefix, visible)
        else:
            self._launch_controller_remote_linux(box_name, box_addr, python_script, prep_script, shell_launch_prefix, visible)
            
    def init_controller(self, box_name=None, visible=False, launch_if_needed=True, ip_addr=None, port=None, demand_script=None):
        if ip_addr:
            box_addr = ip_addr
        else:
            box_addr = box_information.get_box_addr(self.config, box_name)
            ip_addr = self.core.get_ip_addr_from_box_addr(box_addr)
            port = utils.CONTROLLER_PORT

        utils.diag("init_controler: box_name={}".format(box_name))

        if self.is_controller_running(box_addr, port):
            #print("(controller is running)")
            pass    
        elif launch_if_needed:
            # let this always use the standard port (we don't launch on demand on azure-batch machines)
            self._launch_controller(box_name, box_addr, visible, demand_script=demand_script)
            if demand_script:
                # give extra time to do initial processing of runs on main thread
                time.sleep(5)
            else:
                time.sleep(2)
        else:
            return False

        # the controller should now be running - try to connect
        try:
            if not self.conn:
                utils.diag("  connecting to controller")
                self.conn = rpyc.connect(ip_addr, port=port, config = {"allow_public_attrs" : True})

            # magic step: allows our callback to work correctly!
            bgsrv = rpyc.BgServingThread(self.conn)
        except BaseException as ex:
            self.report_controller_init_failure(box_name, box_addr, self.port, ex)
            raise ex     # catch in outer loop

        return True 

    def close_controller(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            
    def report_controller_init_failure(self, box_name, box_addr, port, ex):
        batch_ext = ".bat" if utils.is_windows() else ".sh"

        if utils.is_localhost(box_name, box_addr):
            fn_script = utils.fix_slashes(utils.CONTROLLER_BATCH)
            #fn_log = utils.fix_slashes(utils.CONTROLLER_SCRIPT_LOG)
            fn_log = utils.fix_slashes(utils.CONTROLLER_INNER_LOG)

            print("Exception while trying to connect to LOCAL controller on port: " + str(port) + "; " + str(ex))
            print("\nSuggested steps to debug problem:")
            #print("  1. Ensure that port '{}' is open on {}".format(port, box_addr))
            print("  1. Ensure that the generated script looks correct: {}".format(fn_script))
            print("  2. Check the output of '{}' for errors".format(fn_log))
            print("  3. Try running the script yourself: {}\n".format(fn_script))
        else:
            fn_log = utils.CONTROLLER_INNER_LOG
            print("Exception while trying to connect to REMOTE controller on port: " + str(port) + "; " + str(ex))
            print("\nSuggested steps to debug problem:")
            print("  1. Ensure that port " + str(port) + " is open on " + box_addr)
            print("  2. Check the output of '{}' (on box) for errors\n".format(fn_log))
        
    def kill_controller_by_boxes(self, box_list):
        for box_name in box_list:
            # connect to specified box
            self.change_box(box_name, False)
            self.kill_controller(box_name)

    def get_status_of_runs(self, ws, run_names):
        # use strings to communicate (faster than proxy objects)
        run_names_str = "^".join(run_names)
        #print("run_names_str=", run_names_str)
        json_status_dict = self.conn.root.get_status_of_runs(ws, run_names_str)
        #print("json_status_dict=", json_status_dict)

        box_status_dict = json.loads(json_status_dict)

        return box_status_dict

    def jobs_report(self, ws=None, run_name=None):

        # create helper for filtering runs to show
        builder = ListBuilder(self.config, self.store, self)
        active_only = builder.filtering_active_only()

        # get status from controller
        status_list = self.conn.root.get_status(active_only=active_only, ws_name=ws, run_name=run_name).split("\n")[0:-1]

        if status_list:
            records = []
            for stats in status_list:
                ws, name, status, elapsed = stats.split("^")
                full_name = ws + "/" + name
                #print("full_name=", full_name)

                if not builder.filtered_out(status):
                    elapsed = utils.format_elapsed_hms(elapsed)
                    record = {"name": full_name, "status": status, "elapsed": elapsed}
                    records.append(record)

            result = builder.build_formatted_table(records, avail_cols=["name", "status", "elapsed"])
        else:
            result = "  <none>" + "\n"

        return result

    def upload_file(self, localpath, remotepath, chunk_size = 16000):
        #print("localpath=", localpath, ", remotepath=", remotepath)

        with open(localpath, "rb") as lfile:
            with self.conn.root.open(remotepath, "wb") as rfile:
                while True:
                    buffer = lfile.read(chunk_size)
                    if not buffer:
                        break
                    rfile.write(buffer)        

    def upload_wildcard_files(self, source_wildcard, remotepath, recursive=True, chunk_size = 16000):

        self.conn.root.mkdir(remotepath, False)
        source_wildcard = os.path.expanduser(source_wildcard)

        for fn_source in utils.glob(source_wildcard):
            if os.path.isfile(fn_source):
                fn_remote = remotepath + "/" + os.path.basename(fn_source)
                self.upload_file(fn_source, fn_remote)
            elif os.path.isdir(fn_source) and recursive:
                # copy subdir
                base_dir = os.path.basename(fn_source)
                self.upload_wildcard_files(fn_source + "/*", remotepath + "/" + base_dir)

    def run_local(self, cmd_parts, run_name, exper_name, app_info, job_id, box_name, resume_name, context):
        utils.timing("run_local: start")
        wd = os.path.abspath(".")

        # better to send as JSON
        json_context = json.dumps(context.__dict__)

        result, status = self.conn.root.queue_job(json_context, cmd_parts)
        utils.timing("run_local: after queue_job")

    def run_box(self, user_cmd_parts, run_name, exper_name, app_info, job_id, box_name, resume_name, context):

        # start the job
        utils.diag("  sending controller request to run cmds on box: " + str(user_cmd_parts))

        # better to send as JSON
        json_context = json.dumps(context.__dict__)
        self.conn.root.queue_job(json_context, user_cmd_parts)

    def extract_run(self, ws, run_name, dest_dir):
        #print("ws=", ws, ", run_name=", run_name, ", dest_dir=", dest_dir)

        if os.path.exists(dest_dir):
            utils.user_error("The output directory cannot already exist: " + str(dest_dir))

        files = self.store.download_files_from_run(ws, run_name, "*", dest_dir)
        print(f"{len(files)} files downloaded to: {dest_dir}")

    def status_to_desc(self, run_name, status):
        if status == "queued":
            desc = "{} has been queued".format(run_name)
        elif status == "spawning":
            desc = "{} is spawning repeat runs".format(run_name)
        elif status == "running":
            desc = "{} has started running".format(run_name)
        elif status == "completed":
            desc = "{} has completed".format(run_name)
        elif status == "error":
            desc = "{} has terminated with an error".format(run_name)
        elif status == "killed":
            desc = "{} has been killed".format(run_name)
        elif status == "aborted":
            desc = "{} has been unexpectedly aborted".format(run_name)
        else:
            desc = "{} has unknown status={}".format(run_name, status)

        return "<" + desc + ">"

    def attach_task_to_console(self, ws_name, run_name, show_waiting_msg=False, show_run_name=False):

        full_run_name = ws_name + "/" + run_name

        # callback for each console msg from ATTACHED task
        def console_callback(run_name, msg):
            if msg.startswith(utils.APP_EXIT_MSG):
                #print(msg)
                status = msg.split(":")[1].strip()
                desc = self.status_to_desc(run_name, status)
                print(desc)
                context.remote_app_is_running = False
            else:
                if show_run_name:
                    print(run_name + ": " + msg, end="", flush=True)
                else:   
                    print(msg, end="", flush=True)

        # RPYC bug workaround - callback cannot write to variable in its context
        # but it CAN write to an object's attribute
        context = Bag()
        context.remote_app_is_running = True
        show_detach_msg = False
        detach_requested = False

        attached, status = self.conn.root.attach(ws_name, run_name, console_callback)
        if attached:
            #if show_waiting_msg:
            #    print("\n<attached: {}>\n".format(full_run_name))

            started = time.time()
            timeout = self.config.get("general", "escape")
            if timeout:
                timeout = float(timeout)
    
            try:
                with KeyPressChecker() as checker:
        
                    # ATTACH LOOP
                    while context.remote_app_is_running:
                        if checker.getch_nowait() == 27:
                            detach_requested = True
                            break

                        time.sleep(.1)

                        if timeout:
                            elapsed = time.time() - started
                            if elapsed >= timeout:
                                break


            except KeyboardInterrupt:
                detach_requested = True
            finally:
                self.conn.root.detach(ws_name, run_name, console_callback)

            if detach_requested or show_waiting_msg:
                print("\n<detached from run: {}>".format(full_run_name))
        else:
            desc = self.status_to_desc(run_name, status)
            print(desc)

    def run_job_on_box(self, job_id, run_data_list, box_index, box_info, app_info, pool_info,  
        resume_name=None, demand_mode=False, repeat=None, using_hp=None):

        box_name = box_info.box_name
        #print("box_name=", box_name, ", box_index=", box_index)

        # make everyone think box_name is our current controller 
        #self.change_box(box_name, init_controller)

        if demand_mode:
            # used to test azure-batch mode of running the controller, including:
            # initialization, context file processing, shut-down, and preemption kill/restart.

            # FYI - currently only LOCALHOST supported because we run the generated context file 
            # directly, without copyiing it to the target box)
            tmp_dir = utils.make_tmp_dir("run-demand", True)

            # create the controller context file for this box
            fn_context, run_names = self.core.create_context_file(run_data_list, box_index, job_id, tmp_dir)
            fn_context = utils.fix_slashes(fn_context, force_linux=True)
            hold_open = self.config.get("general", "hold")

            # this command runs the xt controller with a list of runs, described by the filename in fn_context
            xtc_command = "from xtlib.controller import run as run; run({}, {}, '{}', {}, {})" \
                .format(1, None, fn_context, hold_open, utils.CONTROLLER_PORT)  

            # kill controller if already running
            self.kill_controller(box_name)

            # run controller with context file
            self.init_controller(box_name, visible=True, demand_script=xtc_command)
            utils.feedback("connected")  

        else:
            # ensure controller is connected
            self.init_controller(box_name)
            utils.feedback("connected")  

            # loop thru each run for this box
            for run_data in run_data_list:
                #print("run_data=", run_data)

                run_name = run_data["run_name"]
                cmd_parts = run_data["cmd_parts"]
                #exper_name, app_name, app_info = self.core.get_exper_name(cmd_parts)
                exper_name = app_info.exper_name
                app_name = app_info.app_name

                result = None
                box_cmd_parts = cmd_parts 

                utils.feedback("queueing: {}/{}".format(self.ws, run_name.upper()))
                
                box_addr = box_information.get_box_addr(self.config, box_name)
                #print("cmd-parts=", box_cmd_parts)

                context = self.core.get_client_context(exper_name, run_name, app_info, box_info, job_id, node_index=box_index, 
                    cmd_parts=cmd_parts, resume_name=resume_name, using_hp=using_hp, repeat=repeat)

                if utils.is_localhost(box_name, box_addr):
                    self.run_local(cmd_parts, run_name, exper_name, app_info, job_id, box_name, resume_name, context)   
                elif self.config.name_exists("boxes", box_name):
                    self.run_box(cmd_parts, run_name, exper_name, app_info, job_id, box_name, resume_name, context)
                else:
                    utils.user_error("Unknown box name: " + str(box_name))

                utils.feedback("queued", is_final=True)

    def change_box(self, box_name, init_controller=False): 
        #print("change_box: box_name=", box_name)
        
        # temp workarounds....
        self.config.set("core", "box", value=box_name)
        self.box = box_name
        self.core.box = box_name

        # some commands (like 'kill controller') must prevent controller from starting
        if init_controller and not utils.is_azure_batch_box(box_name):
            self.init_controller(box_name)

    def pool_loop(self, boxes, func, init_controller=True):
        results = []

        for b, box_name in enumerate(boxes):
            #print("box_name=", box_name)

            # make everyone think box_name is our current controller 
            self.change_box(box_name, init_controller)

            result = func(box_name, b)
            results.append(result)

        return results

    def monitor_attach_run(self, ws, run_name, show_waiting_msg=True):
        print("")    # separate the waiting loop output from previous output
        attach_attempts = 0

        def monitor_work():
            nonlocal attach_attempts
            azure_task_state, connected, box_name, job_id = self.connect_to_box_for_run(ws, run_name)
            attach_attempts += 1

            #if not connected:
            #    utils.user_exit("Unable to attach to run (state={})".format(state))
            if azure_task_state:
                # its an azure-batch controlled run
                if azure_task_state == "active":
                    text = "Waiting for run to start: {} ({} in azure-batch)".format(run_name.upper(), job_id)
                elif azure_task_state == "running" and not connected:
                    text = "Waiting for run to initialize: {} ({} in azure-batch)".format(run_name.upper(), job_id)
                else:
                    # exit monitor loop
                    return azure_task_state, connected, box_name, job_id, attach_attempts
            else:
                # its a normal box-controller run
                if not connected:
                    utils.error("could not connect to box: " + box_name)
                # we are connected, but has run started yet?
                status_dict = self.get_status_of_runs(ws, [run_name])
                status = status_dict[run_name]
                if status == "queued":
                    text = "Waiting for run to start: {} (queued to run on {})".format(run_name.upper(), box_name)
                else:
                    # status is one of running, killed, completed, spawning, ...
                    # exit monitor loop
                    return azure_task_state, connected, box_name, job_id, attach_attempts
            return text

        # wait for run to be attachable in a MONITOR LOOP
        result = self.monitor_loop(True, monitor_work, "[hit ESCAPE to detach] ")
        #print("")    # separate the waiting loop output from subsequent output  

        if result:
            state, connected, box_name, job_id, attach_attempts = result
            #print("state=", state, ", connected=", connected, ", box_name=", box_name, ", job_id=", job_id)

            if not connected:
                if attach_attempts == 1:
                    utils.user_exit("Unable to attach to run (state={})".format(state))
                else:
                    # not an error in this case
                    print("Unable to attach to run (state={})".format(state))
                    return
                    
            print("<attaching to: {}/{}>\n".format(ws, run_name))
            self.attach_task_to_console(ws, run_name, show_waiting_msg=show_waiting_msg)
        else:
            # None returned; user cancelled with ESCAPE, so no further action needed
            pass    

    def monitor_loop(self, monitor, func, action_msg="monitoring "):
        '''
        set up a loop to continually call 'func' and display its output, until the ESCAPE key is pressed
        '''
        # handle the easy case first
        if not monitor:
            text = func()
            print(text, end="")
            return

        utils.enable_ansi_escape_chars_on_windows_10()

        if monitor == True:
            monitor = 5     # default wait time
        else:
            monitor = int(monitor)
        started = datetime.datetime.now()

        started2 = time.time()
        timeout = self.config.get("general", "escape")
        if timeout:
            timeout = float(timeout)

        last_result = None

        # MONITOR LOOP
        with KeyPressChecker() as checker:
            while True:
                result = func()
                if not isinstance(result, str):
                    # func has decided to stop the monitor loop itself
                    if last_result:
                        print("\n")
                    return result

                if last_result:
                    # erase last result on screen
                    print("\r", end="")
                    line_count = len(last_result.split("\n")) - 1 
                    utils.move_cursor_up(line_count, True)

                elapsed = utils.elapsed_time(started)
                result += "\n" + action_msg + "(elapsed time: {})...".format(elapsed)

                print(result, end="")
                sys.stdout.flush()
                
                if timeout:
                    elapsed = time.time() - started2
                    if elapsed >= timeout:
                        print("\nmonitor timed out")
                        break

                # wait a few seconds during refresh
                if utils.wait_for_escape(checker, monitor):
                    print("\nmonitor cancelled")
                    break

                last_result = result
        return None

    def connect_to_box_for_run(self, ws_name, run_name):
        # get job_id from first log record
        box_name = None
        connected = False
        state = None
        job_id = None

        records = self.store.get_run_log(ws_name, run_name)
        dd = records[0]["data"]
        if utils.is_azure_batch_box(dd["box_name"]):
            job_id = dd["job_id"]
            node_index = dd["node_index"]

            batch = AzureBatch(self.config)
            state, ip_addr, port = batch.get_azure_box_addr(job_id, node_index)
            #print("job_id=", job_id, ", state=", state, ", ip_addr=", ip_addr, ", port=", port)
            if ip_addr:
                box_name = ip_addr + ":" + str(port)
                connected = self.init_controller(ip_addr=ip_addr, port=port, launch_if_needed=False)
        else:
            # normal (non-azure batch) job
            box_name = dd["box_name"]
            #print("box_name=", box_name)
            connected = self.init_controller(box_name=box_name, launch_if_needed=True)

        return state, connected, box_name, job_id

