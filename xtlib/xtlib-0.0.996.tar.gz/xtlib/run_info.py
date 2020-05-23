# run_info.py: information about a run (kept on the controller)
import os
import sys
import copy 
import rpyc
import time 
import json
import psutil
from threading import Thread, Lock

from .store import Store
from . import utils

class RunInfo():
    def __init__(self, run_name, workspace, cmd_parts, prep_script, repeat, context, status, show_output=True, parent_name=None, 
        parent_prep_needed=False):

        if isinstance(repeat, str):
            repeat = int(repeat)

        self.run_name = run_name
        self.parent_name = parent_name
        self.workspace = workspace
        self.cmd_parts = cmd_parts
        self.prep_script = prep_script
        self.repeat = repeat
        self.repeats_remaining = repeat if context.repeats_remaining is None else context.repeats_remaining 
        self.context = context
        self.status = status    
        self.is_wrapped_up = False     # this is set to True by controller when all wrapup processing has completed
        self.show_output = show_output
        self.callbacks = [] 
        self.acallbacks = []
        self.exit_code = None
        self.killing = False
        self.lock = Lock()   
        self.process = None     
        self.store = None    
        self.recent_output = []
        self.max_recent = 10
        self.rundir = None      # assigned at start time
        self.started = time.time()      # time started with current status
        self.elapsed = None
        self.parent_prep_needed = parent_prep_needed      # when True, must run parent prep script before running first child
        self.console_fn = None

        print("run_info ctr: setting self.repeats_remaining=", self.repeats_remaining)
        
    def process_run_output(self, text_msg, run_info_is_locked=False):

        if self.context.scrape:
            # scrape output line for XT log records
            if self.scrape_output(text_msg):
                # don't show scraped output to user
                return

        # let run_info keep recent output for new clients
        self.update_recent_output(text_msg)

        # append to output file
        with open(self.console_fn, "a") as tfile:
            tfile.write(text_msg)

        # send output to attached clients
        if self.show_output:
            if run_info_is_locked:
                list2 = list(self.acallbacks)
            else:
                with self.lock:
                    # make a copy of list for safe enumeration 
                    list2 = list(self.acallbacks)

            # print output on controller console
            sys.stdout.write(self.run_name + ": ")
            sys.stdout.write(text_msg)

            for callback in list2:
                try:
                    callback(self.run_name, text_msg)
                except BaseException as ex:
                    #pass
                    raise ex

    def get_core_properties(self):
        dd = {"run_name": self.run_name, "workspace": self.workspace, "cmd_parts": self.cmd_parts, "prep_script": self.prep_script, 
            "repeat": self.repeat,  "status": self.status, "show_output": self.show_output, "repeats_remaining": self.repeats_remaining,
            "parent_name": self.parent_name}

        context = copy.copy(self.context.__dict__)
        dd["context"] = context

        return dd

    def attach(self, callback):
        self.callbacks.append(callback)       
        acallback = rpyc.async_(callback)

        # first, send recent output 
        #lines = "\n<recent output>\n\n" + "".join(self.recent_output)
        lines = "".join(self.recent_output)
        acallback(self.run_name, lines)

        # now, hook to our list of callback for next output line
        with self.lock: 
            self.acallbacks.append(acallback)           

    def detach(self, callback):
        with self.lock:
            index = self.callbacks.index(callback)
            if index > -1:
                del self.callbacks[index]
                del self.acallbacks[index]

    def update_recent_output(self, msg):
        self.recent_output.append(msg)
        if len(self.recent_output) > self.max_recent:
            self.recent_output = self.recent_output[10:]        # drop oldest 10 lines

    def scrape_output(self, msg):
        '''
            format 1 (xt custom): xt.metrics: epoch=2, test-acc=0.8642270192747726
            format 2 (xt custom): @xtlog^metrics^{"epoch": 2, "test-acc": 0.8642270192747726}
        '''

        event = None
        data_dict = None

        # format 1
        if msg.startswith("xt.") and ":" in msg and "=" in msg:
            msg = msg[3:]       # skip over "xt." prefix
        
            # extract event name
            index = msg.find(":")
            event = msg[0:index]    # extract event name

            # build data dict of name/value pairs
            data_dict = {}
            msg = msg[index+1:]
            cparts = msg.split(",")
            for cp in cparts:
                eparts = cp.split("=")
                if len(eparts) != 2:
                    return
                key = eparts[0].strip()
                value = eparts[1].strip()
                data_dict[key] = value
        # format 2
        elif msg.startswith("@xtlog^"):
            parts = msg.split("^")
            if len(parts) == 3:
                event = parts[1]
                data_dict = json.loads(parts[2])

        # append to run log   
        found = event and data_dict
        if found:       
            context = self.context
            if not self.store:
                self.store = Store(context.store_path, context.store_key)
            self.store.log_run_event(context.ws, self.run_name, event, data_dict)

        return found

    def wrapup_parent_prep_run(self):
        context = self.context
        store = Store(context.store_path, context.store_key)

        store.log_run_event(context.ws, self.run_name, "parent_prep_script_completed", {"status": self.status})

    def run_wrapup(self):
        '''wrap-up the run (logging, capture)'''

        context = self.context
        run_name = self.run_name
        store = Store(context.store_path, context.store_key)

        self.check_for_completed(True)

        store.wrapup_run(context.ws, run_name, context.aggregate_dest, context.dest_name, self.status, self.exit_code, 
            context.metric_rollup_dict, self.rundir, context.after_files_list, context.log, context.capture)

    def set_status(self):
        if self.killing:
            self.status = "killed"
        elif self.exit_code:
            self.status = "error"
        else:
            self.status = "completed"

        self.elapsed = time.time() - self.started
        #print("set_status: status=", self.status)

    def check_for_completed(self, wait_if_needed=False):
        result = None
        if self.process:

            # wait for process to completely terminate
            if wait_if_needed:
                print("waiting for process to terminate...")
                self.process.wait()

            presult = self.process.poll()
            print("process.poll() result=", presult)

            if presult or wait_if_needed:
                # terminated
                self.exit_code = self.process.returncode
                self.process = None
                self.set_status()
                result = True  # "completed (exit code=" + str(self.exit_code) + ")"
            elif self.killing:
                self.status = "dying"   
        return result

    def get_summary_stats(self):
        self.check_for_completed()
        elapsed = self.elapsed if self.elapsed else time.time() - self.started
        return "{}^{}^{}^{}".format(self.workspace, self.run_name, self.status, elapsed)

    def set_process(self, process):
        self.process = process
        self.status = "running"
        print("set_process for {}, pid={}".format(self.run_name, self.process.pid))

    def kill(self):

        result = False
        print("run_info: self.status=", self.status, ", self.process=", self.process)

        if self.process:
            result = self.check_for_completed()

            if not result and self.process and self.process.pid:
                self.killing = True

                # convert popen object to real Process object
                print("processing kill request for {}, pid={}".format(self.run_name, self.process.pid))

                # allow for "no such process" exception due to timing errors
                try:
                    p = psutil.Process(self.process.pid)

                    # since we run job in a batch file, we need to enumerate all kill
                    # all child processes
                    kids = p.children(recursive=True)
                    for kid in kids:
                        print("  killing CHILD process, pid=", kid.pid)
                        kid.kill()
                except psutil.NoSuchProcess as ex:
                    print("run={}, exception while killing process: {}".format(self.run_name, ex))

                # it may have changed async since above check (Ricky has seen this issue)
                if self.process and self.process.pid:
                    print("  killing MAIN process, pid=", self.process.pid)
                    self.process.kill()
                
                result = self.check_for_completed()
                #self.exit_code = self.process.returncode
                #self.process = None
                #self.status = "killed"
                result = True   # "killed! (exit code=" + str(self.exit_code) + ")"
        elif self.status in ["queued", "spawning", "running"]:
            self.status = "killed"
            self.elapsed = time.time() - self.started

             # must call manually since it doesn't have a process exit_handler()
            self.run_wrapup()          
            result = True   
        elif self.status in ["completed", "error", "killed", "aborted"]:
            result = False   # nothing for us to do
        else:
            print("run_info.kill: unexpected status=", self.status)

        return result, self.status

