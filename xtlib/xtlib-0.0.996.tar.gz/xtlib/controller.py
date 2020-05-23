# controller.py - running on the compute box, controls the management of all XT or XTLib initiated jobs for that machine.
import sys
import os
import json
import rpyc
import copy
import time
import shutil 
import random
import subprocess
import datetime
from threading import Thread, Lock
from rpyc.utils.server import ThreadedServer

from .helpers.bag import Bag
from .helpers.stream_capture import StreamCapture
from .store import Store
from .run_info import RunInfo
from . import utils

'''
Our controller is implemented as a Service so that client apps (XT and XTLib apps) from the same or different machines 
can connect to it.  Services offered include:
    - start a run  
    - get status of a run
    - enumerate runs on the hosting computer
    - kill a run
    - attach/detach to run's streaming console output
    - run a command on the box
    - copy files to/from box
'''

# constants
DETACHED_PROCESS = 0x00000008

queue_lock = Lock()            
runs_lock = Lock()            
rundir_lock = Lock()

def read_from_pipe(pipe, console_fn, run_info, runner, stdout_is_text):
    #print("------------------>  read_from_pipe started, console_fn=", console_fn, ", stdout_is_text=", stdout_is_text)

    # expand any "~" in path
    console_fn = os.path.expanduser(console_fn)
    run_info.console_fn = console_fn

    if os.path.exists(console_fn):
        os.remove(console_fn)

    run_name = run_info.run_name

    while True:
        if stdout_is_text:
            text_msg = pipe.readline()
            # # try to detect progress-style lines which originally had only CR at end
            # if "\r" in pipe.newlines and "%" in text_msg and text_msg[-2] == "]":
            #     # restore CR only char
            #     text_msg = text_msg.replace("\n", "\r")
        else:
            binary_msg = pipe.readline()
            text_msg = binary_msg.decode("utf-8")

        if len(text_msg) == 0 or run_info.killing:
            break      # EOF / end of process

        run_info.process_run_output(text_msg)

    # run post-processing
    runner.exit_handler(run_info)

class MyService(rpyc.Service):

    def __init__(self, max_runs=1, my_ip_addr=None, multi_run_context_fn=None, multi_run_hold_open=False, 
            port=None, *args, **kwargs):
        self.max_runs = max_runs
        self.killing_process = False
        self.started = time.time()
        self.rundirs = {}
        self.rundir_parent = os.path.expanduser("~/.xt/rundirs")
        self.my_ip_addr = my_ip_addr
        self.shutdown_requested = None
        self.queue_check_count = 0
        self.state_changed = False
        
        self.runs = {}       # all runs that we know about (queued, spawing, running, or completed)
        self.queue = []      # runs that are waiting to run (due to max_runs)

        # for azure batch runs
        self.multi_run_context_fn = multi_run_context_fn
        self.multi_run_hold_open = multi_run_hold_open
        self.job_id = 0
        self.node_index = 0

        fn_inner_log = os.path.expanduser(utils.CONTROLLER_INNER_LOG)
        utils.ensure_dir_exists(file=fn_inner_log)

        # capture STDOUT
        self.cap_stdout = StreamCapture(sys.stdout, fn_inner_log, True)
        sys.stdout = self.cap_stdout

        # capture STDERR
        self.cap_stderr = StreamCapture(sys.stderr, True, file=self.cap_stdout.log_file)
        sys.stderr = self.cap_stderr

        print("XT Controller ({})".format(utils.BUILD))
        print(datetime.datetime.now())

        print("max_runs={}, my_ip_addr={}, multi_run_context_fn={}, multi_run_hold_open={}, port={}".format(
            max_runs, my_ip_addr, multi_run_context_fn, multi_run_hold_open, port))
           
        utils.ensure_dir_exists(self.rundir_parent)

        # NOTE: do NOT add "store" as a class or instance member since it may vary by run/client
        # it should just be created when needed (at beginning and end of a run)

        super(MyService, self).__init__(*args, **kwargs)

        if multi_run_context_fn:
            self.process_multi_run_context(multi_run_context_fn)

        # start a queue manager thread to start jobs as needed
        stdout_thread = Thread(target=self.thread_manager)
        stdout_thread.start()

    def get_checkpoint_fn(self, node_index):
        fn = "node-{}/xt-controller-checkpoint.json".format(node_index)
        return fn

    def checkpoint_state(self):
        # make a checkpoint of our current state in case we have to restart

        with runs_lock:
            runs = [r.get_core_properties() for r in self.runs.values()]

        # if we have no runs, we cannot write a checkpoint (need job_id and node_index)
        if runs:
            # for now, borrow the store from our first run
            context = utils.dict_to_object(runs[0]["context"])
            store = Store(context.store_path, context.store_key)

            state = {"runs": runs}
            state_str = json.dumps(state)

            # upload our checkpoint data
            node_index = 0 if context.node_index is None else context.node_index
            store_path = self.get_checkpoint_fn(node_index)
            store.create_job_file(context.job_id, store_path, state_str)

            print("checkpoint written to: job={}, path={}".format(context.job_id, store_path))

    def on_state_changed(self):
        # may want to use a timer to buffer this
        self.state_changed = True

    def get_checkpoint_info(self, store, job_id, node_index):
        cp_data = None
        info_by_run = {}
        store_path = self.get_checkpoint_fn(node_index)
        cp_exists = store.does_job_file_exist(job_id, store_path)

        print("get_checkpoint_info: path={}, exists={}".format(store_path, cp_exists))

        if cp_exists:
            text = store.read_job_file(job_id, store_path)
            cp_data = json.loads(text)

        return cp_exists, cp_data

    def process_multi_run_context(self, multi_run_context_fn):
        # read the cmd and context from the file
        print("found multi_run_context file")

        with open(multi_run_context_fn, "rt") as tfile:
            text = tfile.read()

        mrc_data = json.loads(text)
        # mrc_data = {"job_id": job_id, "node_index": node_index, "runs": node_runs}
        self.job_id = mrc_data["job_id"]
        self.node_index = mrc_data["node_index"]

        # need to create a store object; borrow context from first run
        context = utils.dict_to_object(mrc_data["runs"][0])
        store = Store(context.store_path, context.store_key)

        cp_exists, cp_data = self.get_checkpoint_info(store, self.job_id, self.node_index)
        was_queued = []    # list of runs that were queued before we were restarted

        if cp_exists:
            self.restart_checkpoint_runs(store, cp_data)
        else:
            self.start_local_runs_from_mrcfile(store, mrc_data)
    
    def start_local_runs_from_mrcfile(self, store, mrc_data):
        # queue each run in mrc_data
        for run_context in mrc_data["runs"]:
            #print("run_context=", run_context)

            context = utils.dict_to_object(run_context)
            cmd_parts = context.cmd_parts

            # queue this run 
            self.queue_job_core(context, cmd_parts)

    def restart_checkpoint_runs(self, store, cp_data):
        # rely on checkpoint state to know which runs to start and restart
        was_queued = []
        print("--- processing checkpoint runs ---")

        for run_data in cp_data["runs"]:

            run_name = run_data["run_name"]
            status = run_data["status"]
            context = utils.dict_to_object(run_data["context"])
            repeats_remaining = run_data["repeats_remaining"]

            print("  process checkpoint run: name={}, status={}, repeats_remaining={}".format(run_name, status, repeats_remaining))

            # no processing needed if run as ended
            if status in ["completed", "killed", "aborted", "error", "unknown"]:
                continue

            if context.is_parent:
                # parent run 
                context.repeats_remaining = repeats_remaining
                print("  found parent run: repeat={}, setting repeats_remaining={}".format(context.repeat, context.repeats_remaining))

            if status == "running":
                # child or flat run
                # tell this run that he restarting, and give him his own run as resume source
                context.restart = True
                context.resume_name = run_name   
                print("  found child or flat run: setting resume_name=", context.resume_name)

            if status in ["spawning", "queued"]:
                was_queued.append(context)
                print(" added run to was_queued")
            else:
                # requeue this run immediately
                print("  (immediate) requeuing: ", run_name)
                self.queue_job_core(context, context.cmd_parts)

        # now queue previously queued jobs (to keep order approx. correct)
        print("processing was_queued=", was_queued)

        for context in was_queued:
            print("  (at end) requeuing: ", context.run_name)
            self.queue_job_core(context, context.cmd_parts)

        print("--- end of processing checkpoint runs ---")

    def thread_manager(self):
        while True:
            time.sleep(.5)
            self.queue_check(1)
               
    def queue_count(self):
        with queue_lock:
            return len(self.queue)

    def queue_check(self, max_starts=1):
        ''' see if 1 or more jobs at top of queue can be run '''

        # self.queue_check_count += 1
        # print("queue_check # " + str(self.queue_check_count))

        # is it time to shut down the controller?
        if self.multi_run_context_fn and not self.multi_run_hold_open:
            active_count = self.get_active_runs_count()

            if active_count == 0:
                print("processing shutdown request in queue thread...")
                self.checkpoint_state()

                # give other threads time to wrapup the processing of their runs before
                # we exit
                time.sleep(10)    # wait for 10 seconds
                print("calling os._exit(0)...")

                # os._exit will exit all threads without running 'finally' blocks 
                # sys.exit will exit current thread only, but run 'finally' blocks for a cleaner exit
                os._exit(0)

        # for responsiveness, limit # of runs can be released in a single check
        for steps in range(max_starts):       
            running_count = len(self.get_running_names())
            run_info = None

            with queue_lock:
                if len(self.queue):
                    if running_count < self.max_runs or self.max_runs == -1:
                        run_info = self.queue.pop(0)

                        # run_info is ready to run!
                        if run_info.repeat and not run_info.parent_prep_needed:
                            run_info.status = "spawning"
                        else:
                            run_info.status = "running"
                            run_info.started = time.time()

            if run_info:
                if run_info.parent_prep_needed:
                    self.start_local_run(run_info, cmd_parts=[])
                elif run_info.repeat is not None:
                    self.run_template(run_info)
                else:
                    # start normal run
                    self.start_local_run(run_info, cmd_parts=run_info.cmd_parts)

                self.on_state_changed()
            else:
                break

        # process the state_changed flag
        if self.state_changed:
            self.state_changed = False
            self.checkpoint_state()

    def add_to_runs(self, run_info):
        key = run_info.workspace + "/" + run_info.run_name
        with runs_lock:
            self.runs[key] = run_info

        self.on_state_changed()

    def run_template(self, run_info):
        # spawn child run from template
        child_info = self.spawn_child(run_info)
        child_name = child_info.run_name

        # add to runs
        self.add_to_runs(child_info)

         # start normal run of CHILD
        self.start_local_run(child_info, cmd_parts=child_info.cmd_parts)

        # decide if parent (run_info) is finished
        with queue_lock:
            with run_info.lock:
                if run_info.status == "spawning":        # if not cancelled/killed
                    if run_info.repeat == -1:
                        # repeat forever, so insert back into queue
                        self.queue.append(run_info)
                        run_info.status = "queued"
                    else:
                        run_info.repeats_remaining -= 1
                        if run_info.repeats_remaining > 0:
                            # insert back into queue
                            self.queue.append(run_info)
                            run_info.status = "queued"
                        else:
                            # mark as completed
                            print("marking --repeat parent as completed: ", run_info.run_name)
                            run_info.status = "completed"

                            #run_info.run_wrapup()
                            self.exit_handler(run_info, True)


    def requeue_run(self, run_info):
        with queue_lock:
            self.queue.append(run_info)
            run_info.status = "queued"

        print("run requeued: " + run_info.run_name)

    def schedule_controller_exit(self):
        if self.multi_run_hold_open:
            print("holding controller open after single run...")
        else:
            print("xt controller - scheduling shutdown..")
            self.shutdown_requested = True

    def update_cmd(self, cmd_parts, arg_prefix, arg, value):
        prefix = arg_prefix + arg 
        prefix_eq = prefix + "="

        # remove previous arg, if present
        for i, part in enumerate(cmd_parts):
            if part == prefix or part.startswith(prefix_eq):
                del cmd_parts[i]
                break

        # add new arg to end
        part = prefix_eq + str(value)
        cmd_parts.append(part)

    def sample_hparam_value(self, rand, values):
        if len(values) == 1:
            value = values[0]
            if value == "randint":
                value = rand.randint(0, 999999999)
            else:
                value = utils.make_numeric_if_possible(value)
        else:
            index = rand.randint(0, len(values)-1)
            value = utils.make_numeric_if_possible(values[index])

        if isinstance(value, str):
            value = value.strip()
            if " " in value:
                # surround with quotes so it is treated as a single entity
                value = '"' + value + '"'
        return value

    def add_sweep_params_to_cmd(self, cmd_parts, store, context):
        if context.aggregate_dest == "experiment":
            text = store.read_experiment_file(context.ws, context.dest_name, context.hp_config)
        else:    # assume sweeps file is at the job level
            text = store.read_job_file(context.dest_name, context.hp_config)
        #print("sweep text=", text)

        # parse property/value lists and sample a value for each property
        new_lines = []
        rand = random.Random(time.time())

        for orig_line in text.split("\n"):
            line = orig_line.strip()
            if line and not line.startswith("#"):

                # remove comment from end of line
                if "#" in line:
                    line = line.split("#")[0]

                # at this point, line must be pattern: prop = value 
                if "=" in line:
                    parts = line.split("=")
                    if len(parts) != 2:
                        continue     # too many equal signs - skip over line

                    prop, value_str = parts

                    prop = prop.strip()
                    value_str = value_str.strip()
                    values = value_str.split(",")

                    # sample value
                    value = self.sample_hparam_value(rand, values)

                    # update cmd
                    if context.arg_prefix != None:
                        self.update_cmd(cmd_parts, context.arg_prefix, prop, value)

                    # update new config file text
                    new_line = prop + " = " + str(value)
            else:
                new_line = orig_line

            new_lines.append(new_line)
        
        text = "\n".join(new_lines) + "\n"
        print("new sweep text=\n", text)
        return text

    def get_cmd_from_sweeps_list(self, store, context, parent):
        cmd_parts = []

        # read cmds from SWEEPS LIST file
        text = store.read_job_file(context.job_id, utils.HP_SWEEP_LIST_FN)
        cmd_sets_by_node = json.loads(text)

        # get info for this box's node index
        node_id = "node" + str(context.node_index)
        print("sweeps_list: looking for node=", node_id)
        if node_id in cmd_sets_by_node:
            cmd_sets = cmd_sets_by_node[node_id]

            # get cmd for next child run on this box
            run_index = parent.repeat - parent.repeats_remaining
            print("run_index=", run_index, ", cmd_sets=", cmd_sets)
            if run_index >= 0:
                cmd_parts = cmd_sets[run_index]

        return cmd_parts

    def spawn_child(self, parent):
        spawn_start = time.time()

        # create a child run_info from the parent template
        context = copy.copy(parent.context)
        context.repeat = None

        store = Store(context.store_path, context.store_key)

        cmd_parts = list(context.cmd_parts)
        sweep_text = None

        if context.hp_config:
            sweep_text = self.add_sweep_params_to_cmd(cmd_parts, store, context)

            # update context (critical if this run gets preempted/restarted)
            context.cmd_parts = cmd_parts
        elif context.using_hp:
            cmd_parts = self.get_cmd_from_sweeps_list(store, context, parent)
        # create a CLONE of template as a child run
        start_child_start = time.time()

        child_name = store.start_child_run(context.ws, parent.run_name, context.exper_name,
            box_name=context.box_name, app_name=context.app_name,
            from_ip=context.from_ip, from_host=context.from_host, 
            job_id=context.job_id, pool=context.pool, node_index=context.node_index, 
            aggregate_dest=context.aggregate_dest)

        # must update context info
        context.run_name = child_name

        utils.print_elapsed(start_child_start, "START CHILD RUN")
        
        # log run CMD
        store.log_run_event(context.ws, child_name, "cmd", {"cmd": cmd_parts})

        if sweep_text:
            fn_target = context.hp_config
            # upload config file for sweep args to child-specific BEFORE folder
            store.create_run_file(context.ws, child_name, 
                "before/" + fn_target, sweep_text)

        # get_client_context() should have set this correct for this parent/child run
        prep_script = context.child_prep_script     

        child_info = RunInfo(child_name, context.ws, cmd_parts, prep_script, 
            None, context, "running", True, parent_name=parent.run_name)

        utils.print_elapsed(spawn_start, "SPAWN CHILD")

        parent.process_run_output("spawned: {}\n".format(child_name))

        return child_info
 
    def exit_handler(self, run_info, run_info_is_locked=False):
        if run_info.parent_prep_needed:
            print("parent prep script exited")
            run_info.wrapup_parent_prep_run()
        else:
            print("app exited: " + run_info.run_name)

            run_info.run_wrapup()

            # send "app exited" msg to callbacks
            msg = utils.APP_EXIT_MSG + run_info.status + "\n"
            run_info.process_run_output(msg, run_info_is_locked)

        run_info.check_for_completed(True)

        # release rundir
        if run_info.rundir:
            self.return_rundir(run_info.rundir)
            run_info.rundir = None

        # if run_info == self.single_run:
        #     self.schedule_controller_exit()

        self.on_state_changed()

        if run_info.parent_prep_needed:
            run_info.parent_prep_needed = False

            print("run={}, status={}".format(run_info.run_name, run_info.status))

            if run_info.status == "completed":
                # now that the parent prep script has successfully run we can 
                # requeue parent run to spawn child runs
                self.requeue_run(run_info)
        else:
            run_info.is_wrapped_up = True

    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        #print("client attach!")
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        #print("client detach!")
        pass

    def find_file_in_path(self, name):
        path_list = os.getenv('PATH', '')
        #print("path_list=", path_list)

        if utils.is_windows():
            paths = path_list.split(";")
        else:
            paths = path_list.split(":")

        full_fn = None

        for path in paths:
            fn = path + "/" + name
            #print("testing fn=", fn)

            if os.path.exists(fn):
                full_fn = fn
                #print("match found: fn=", full_fn)
                break
        
        return full_fn

    def exposed_elapsed_time(self):
        return time.time() - self.started

    def exposed_xt_version(self):
        return utils.BUILD

    def exposed_controller_log(self):
        fn = os.path.expanduser(utils.CONTROLLER_INNER_LOG)
        with open(fn, "r") as textfile:
            text = textfile.read()
        return text

    def copy_bag(self, bag):
        new_bag = Bag()
        for key,value in bag.get_dict().items():
            setattr(new_bag, key, value)

        return new_bag

    def copy_dict(self, dict):
        new_dict = {}
        for key,value in dict.items():
            new_dict[key] = value

        return new_dict

    def allocate_rundir(self, run_name):
        rundir = None
        base_name = "rundir"

        with rundir_lock:
            for dirname, rn in self.rundirs.items():
                if not rn:
                    # it's available - mark it as in-use
                    self.rundirs[dirname] = run_name
                    rundir = dirname
                    break

            if not rundir:
                # add a new name
                rundir = base_name + str(1 + len(self.rundirs))
                self.rundirs[rundir] = run_name
                print("allocated a new rundir=", rundir)

            print("updated rundirs=", self.rundirs)

        start = len(base_name)
        run_index = int(rundir[start:])
        runpath = self.rundir_parent + "/" + rundir

        # remove and recreate for a clear start for each run
        if os.path.exists(runpath):
            shutil.rmtree(runpath)
        utils.ensure_dir_exists(runpath)

        return runpath, run_index

    def return_rundir(self, rundir_path):
        rundir = os.path.basename(rundir_path)

        with rundir_lock:
            assert (rundir in self.rundirs)

            # mark as no longer used
            self.rundirs[rundir] = None

    def exposed_queue_job(self, json_context, cmd_parts):
        context = json.loads(json_context)
        context = utils.dict_to_object(context)

        # make a copy of cmd_parts
        cmd_parts = list(cmd_parts)
        context.cmd_parts = cmd_parts
        
        run_info = self.queue_job_core(context, cmd_parts)
        return True, run_info.status

    def queue_job_core(self, context, cmd_parts):

        run_name = context.run_name
        exper_name = context.exper_name
        print("queue_job_core: run_name=", run_name, ", context.repeat=", context.repeat)

        #working_dir = os.path.expanduser(context.working_dir)
        app_name = context.app_name
        prep_script = context.prep_script

        # apply specify max_runs when job is queued
        if context.max_runs is not None:
            print("--> setting self.max_runs =", context.max_runs)
            self.max_runs = context.max_runs

        if context.is_parent:
            prep_script = context.parent_prep_script
            parent_prep_needed = True
        else:
            parent_prep_needed = False

        run_info = RunInfo(run_name, context.ws, cmd_parts, prep_script, context.repeat, context, "queued", True, 
            parent_name=None, parent_prep_needed=parent_prep_needed)

        # log run QUEUED event 
        store = Store(context.store_path, context.store_key)
        store.log_run_event(context.ws, run_name, "queued", {})

        # queue job to be run
        with queue_lock:
            self.queue.append(run_info)
            print("after queuing job, queue=", self.queue)

        self.add_to_runs(run_info)

        print("------ run QUEUED: " + run_name + " -------")
        
        # before returning - see if this run can be started immediately
        #self.queue_check(1)

        return run_info 

    def start_local_run(self, run_info, cmd_parts):
        print("start_local_run: run_name=", run_info.run_name, ", cmd_parts=", cmd_parts)

        flat_cmd = " ".join(cmd_parts)

        context = run_info.context  
        run_name = run_info.run_name

        # we need to support multiple run directories (for max_runs param) - so we cannot run in originating dir
        rundir, run_index = self.allocate_rundir(run_name)
        run_info.rundir = rundir

        # download files from STORE to rundir
        store = Store(context.store_path, context.store_key)
        print("downloading BEFORE files from STORE to rundir: run_name=", run_name, ", rundir=", rundir)

        if context.using_hp:
            # all files contained in JOB BEFORE
            files = store.download_files_from_job(context.job_id, "before/**", rundir)
            print("  " + str(len(files)) + " files downloaded from store (JOB dir)")
        else:
            if "." in run_name:
                # download from parent's RUN before files
                parent_name = run_name.split(".")[0]
                files = store.download_files_from_run(context.ws, parent_name, "before/**", rundir)
                print("  " + str(len(files)) + " files downloaded from store (PARENT'S RUN dir)")
            
            # download from normal/child RUN before files
            files = store.download_files_from_run(context.ws, run_name, "before/**", rundir)
            print("  " + str(len(files)) + " files downloaded from store (RUN dir)")

        # if context.xtlib_capture:
        #     # download xtlib files from job
        #     local_dir = os.path.expanduser("~/ExperimentTools/xtlib")
        #     files = store.download_files_from_job(context.job_id, "xtlib/**", local_dir)
        #     print("  " + str(len(files)) + " XTLIB files downloaded from store (JOB dir)")

        # log run STARTED event 
        store = Store(context.store_path, context.store_key)
        start_event_name = "restarted" if context.restart else "started"
        store.log_run_event(context.ws, run_name, start_event_name, {})
        prep_script = run_info.prep_script  

        exper_name = context.exper_name

        # docker login needed?
        if context.docker_login:
            login_cmd = "docker login {} --username {} --password {}".format(context.docker_server, context.docker_username, context.docker_password)
            if not utils.is_windows():
                login_cmd = "sudo " + login_cmd

            prep_script.append(login_cmd)

        # local function
        def safe_env_value(value):
            return "" if value is None else str(value)

        # pass xt info to the target app (these are access thru Store "running" API's)
        child_env = os.environ.copy()
        child_env["XT_WORKSPACE_NAME"] = safe_env_value(context.ws)
        child_env["XT_RUN_NAME"] = safe_env_value(run_name)
        child_env["XT_EXPERIMENT_NAME"] = safe_env_value(exper_name)

        child_env["XT_TARGET_FILE"] = safe_env_value(context.target_file)
        child_env["XT_RESUME_NAME"] = safe_env_value(context.resume_name)

        child_env["XT_STORE_TYPE"] = safe_env_value(context.store_type)
        child_env["XT_STORE_PATH"] = safe_env_value(context.store_path)
        child_env["XT_STORE_KEY"] = safe_env_value(context.store_key)

        print("\nprep_script:\n", prep_script)
        
        if utils.is_windows():
            fn_script = os.path.expanduser("~/.xt/run_app{}.bat".format(run_index))
            utils.send_cmd_as_script_to_box(self, "localhost", flat_cmd, fn_script, prep_script, False)
        else:
            fn_script = os.path.expanduser("~/.xt/run_app{}.sh".format(run_index))
            utils.send_cmd_as_script_to_box(self, "localhost", flat_cmd, fn_script, prep_script, True)

        console_fn = rundir + "/console.txt"

        if os.path.exists(console_fn):
            os.remove(console_fn)

        print("start_local_run running: ", run_name, ", ws=", context.ws, ", target=", child_env["XT_TARGET_FILE"])

        # use False if we want to capture TDQM output correctly (don't convert CR to NEWLINE's)
        stdout_is_text = True
        bufsize = -1 if stdout_is_text else -1     # doesn't seem to affect TDQM's turning off progress logging...

        shell_launch_prefix = context.shell_launch_prefix

        if utils.is_windows():
            # run as dependent process with HIDDEN WINDOW
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            #print("startupinfo=", startupinfo)
            parts = [fn_script]
            print("LOCAL: running cmd:", flat_cmd, ", parts=", parts, ", wd=", rundir)

            process = subprocess.Popen(parts, cwd=rundir, startupinfo=startupinfo, 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=child_env, universal_newlines=stdout_is_text, bufsize=bufsize)
        else:
            #parts = ["/bin/sh", "--login", fn_script]
            if not shell_launch_prefix:
                shell_launch_prefix = "/bin/sh --login"
            parts = shell_launch_prefix.split(" ") + [fn_script]

            print("rundir=", rundir, ", parts=", parts)
            print("fn_script=", fn_script, ", os.path.exists(fn_script)=", os.path.exists(fn_script))
            print("LOCAL: running cmd:", flat_cmd, ", parts=", parts, ", wd=", rundir)

            process = subprocess.Popen(parts, cwd=rundir, 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=child_env, universal_newlines=stdout_is_text, bufsize=bufsize)

        with run_info.lock:
            run_info.set_process(process)

        # start a thread to consume STDOUT and STDERR from process
        stdout_thread = Thread(target=read_from_pipe, args=(process.stdout, console_fn, run_info, self, stdout_is_text))
        stdout_thread.start()

        print("------ run STARTED: " + run_name + " -------")
        return True

    def diag(self, msg):
        print(msg)

    def get_run_info(self, ws_name, run_name, raise_if_missing=True):
        key = ws_name + "/" + run_name
        with runs_lock:
            if key in self.runs:
                return self.runs[key]
            elif raise_if_missing:
                raise Exception("unknown run_name: " + ws_name + "/" + run_name)
        return None

    def exposed_attach(self, ws_name, run_name, callback):
        run_info = self.get_run_info(ws_name, run_name)

        # taking lock here hangs this thread (.attach also takes the lock)
        status = run_info.status
        if (status != "running"):
            return False, status
        run_info.attach(callback)

        return True, status

    def exposed_detach(self, ws_name, run_name, callback):
        run_info = self.get_run_info(ws_name, run_name)
        run_info.detach(callback)

    def exposed_get_status_of_runs(self, ws, run_names_str):
        status_dict = {}
        run_names = run_names_str.split("^")

        for run_name in run_names:
            run_info = self.get_run_info(ws, run_name, False)
            if run_info:
                status_dict[run_name] = run_info.status

        json_status_dict = json.dumps(status_dict)
        return json_status_dict

    def exposed_get_status(self, active_only=False, ws_name=None, run_name=None):
        if run_name:
            print("get_status: ws_name=", ws_name, ", run_name=", run_name)

            run_info = self.get_run_info(ws_name, run_name)
            return run_info.get_summary_stats() + "\n"
        else:
            result = ""
            with runs_lock:
                for run_info in self.runs.values():
                    status = run_info.status
                    if active_only:
                        if status in ["queued", "spawning", "running"]:
                            result += run_info.get_summary_stats() + "\n"
                    else:
                        result += run_info.get_summary_stats() + "\n"
                return result

    def kill_core(self, run_info):
        print("---- killing: {}/{} -----".format(run_info.workspace, run_info.run_name))

        with queue_lock:
            if run_info in self.queue:
                self.queue.remove(run_info)

        # log run KILLED event 
        context = run_info.context
        store = Store(context.store_path, context.store_key)
        store.log_run_event(context.ws, run_info.run_name, "killed", {})

        with run_info.lock:
            try:
                result, status = run_info.kill()
            except BaseException as ex:
                print("{}: got exception while trying to kill process; ex={}".format(run_info.run_name, ex))

        print("run_info.kill returned result=", result, ", status=", status)
        
        # if run_info == self.single_run:
        #     self.schedule_controller_exit()

        return result, status

    def get_matching_run_infos(self, full_run_names):
        # match all runinfos that have not finished (exact match and matching children)
        matches = []
        full_name_set = set(full_run_names)

        with runs_lock:
            running = [ri for ri in self.runs.values() if ri.status in ["running", "spawning", "queued"]] 

        for ri in running:
            base_name = ri.run_name.split(".")[0]
            if ri.workspace + "/" + base_name in full_name_set:
                # match parent to parent or child to parent
                matches.append(ri)
            elif ri.workspace + "/" + ri.run_name in full_name_set:
                # exact parent/child name match
                matches.append(ri)

        print("matches=", matches)
        return matches

    def kill_all(self):
        to_kill = []
        results = []

        # loop until we are IDLE
        while True:
            with queue_lock:
                to_kill += self.queue
                self.queue = []

            # grab all running jobs
            with runs_lock:
                running = [ri for ri in self.runs.values() if ri.status in ["running", "spawning"]] 
                to_kill += running

            if not to_kill:
                # we are IDLE
                print("----------- SYSTEM IDLE ---------------")
                break

            # kill jobs 1 at a time
            while len(to_kill):
                run_info = to_kill.pop(0)
                result, status = self.kill_core(run_info)

                results.append( {"workspace": run_info.workspace, "run_name": run_info.run_name, 
                    "killed": result, "status": status} )

        return results

    def kill_specified_runs(self, full_run_names):
        to_kill = []
        results = []

        # loop until we are IDLE
        while True:

            to_kill = self.get_matching_run_infos(full_run_names)

            if not to_kill:
                # we are IDLE
                print("----------- SPECIFIED RUNS ARE IDLE ---------------")
                break

            # kill jobs 1 at a time
            while len(to_kill):
                run_info = to_kill.pop(0)
                result, status = self.kill_core(run_info)

                results.append( {"workspace": run_info.workspace, "run_name": run_info.run_name, 
                    "killed": result, "status": status} )

        return results

    def exposed_kill_run(self, run_names):
        results = []

        if run_names == "all":
            results = self.kill_all()
        else:
            # kill specific run(s)
            results = self.kill_specified_runs(run_names)

        # send results as json text so that client is not tied to controller (which may be killed immediately after this call)
        results_json_text = json.dumps(results)
        return results_json_text

    # used for uploading files to controller (still used?)
    def exposed_open(self, path, flags):
        print("exposed_open: path=", path, ", flags=", flags)
        path = os.path.expanduser(path)
        return open(path, flags)

    # used for uploading files to controller (still used?)
    def exposed_mkdir(self, path, raise_error_if_exists=False):
        print("exposed_mkdir: path=", path)
        path = os.path.expanduser(path)

        dir_exists = os.path.exists(path) and os.path.isdir(path)
        if raise_error_if_exists or not dir_exists:
            os.mkdir(path)

    def exposed_get_ip_addr(self):
        addr = self.my_ip_addr
        if not addr:
            addr = utils.get_ip_address()
        return addr

    def exposed_get_max_runs(self):
        return self.max_runs

    def exposed_set_max_runs(self, value):
        #print("exposed_set_max_runs: value=", value, ", type(value)=", type(value))
        self.max_runs = value

    def get_running_names(self):
        with runs_lock:
            running_names = [run.run_name for run in self.runs.values() if run.status == "running"]
        return running_names

    def get_active_runs_count(self):
        ''' return runs that are:
            - queued
            - spawning
            - running
            - completed but not yet wrapped up
        '''
        with runs_lock:
            active_names = [run.run_name for run in self.runs.values() if not run.is_wrapped_up]
        return len(active_names)

def run(max_runs=1, my_ip_addr=None, multi_run_context_fn=None, multi_run_hold_open=False, port=utils.CONTROLLER_PORT):
    '''
    Runs the XT controller app - responsible for launch and control of all user ML apps for a
    local machine, remote machine, Azure VM, or Azure Batch VM.

    'max-runs' is the maximum number of jobs the controller will schedule to run simultaneously.

    'my_ip_addr' is the true IP address of the machine (as determined from the caller).

    'multi_run_context_fn' is used with Azure Batch - when specified, the controller
       should launch a single job, described in the context file (multi_run_context_fn), and when the job
       is finished, the controller should exit.
    '''
    # port = utils.CONTROLLER_PORT
    # args = sys.argv
    # if len(args) > 1:
    #     port = int(args[1])

    protocol_config = {"allow_public_attrs" : True}

    service = MyService(max_runs, my_ip_addr, multi_run_context_fn, multi_run_hold_open, port)

    t = ThreadedServer(service, port=port, protocol_config=protocol_config)
    t.start()

if __name__ == "__main__":      
    run()
