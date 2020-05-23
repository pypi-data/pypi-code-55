# store.py - implements the STORE API of Experiment Tools

import os
import sys
import time
import json
import uuid
import arrow
import shutil
import socket 

from .helpers.stream_capture import StreamCapture
from .helpers.bag import Bag
from .helpers.part_scanner import PartScanner
from .store_file import StoreFile
from .store_azure_blob import StoreAzureBlob
from .utils import WORKSPACE_DIR, WORKSPACE_LOG, RUN_LOG
from .utils import RUN_STDOUT, RUN_STDERR
from . import utils

# NOTE: *.log files are a list of JSON string records (to make legal, surround with "[]")

# internal utility functions

def _get_time():
    #return time.time()
    return str(arrow.now()) 

# main class that implements the XT STORE API
class Store():
    '''This class provides access to the XT Store, which can be based on either:
        - a local directory
        - Azure Storage service
        - Azure ML Workspace
    Methods are provided to manage workspaces, experiments, runs, and related files.

    You can create an instance of XTStore by providing any of these:
        - a XTConfig instance (holds information from the XT configuration file)
        - the root directory of the XT Store ("file-store" Store)
        - the Azure Storage service name and key ("azure" Store)
        - the Azure Subscription id and resource groupu ("aml" Store)

    :param ws_root_path: the path of the file based store, or the name of the Azure Storage service.
    :param azure_key: the Azure storage key.
    :param sas_token: if this Storage service is being shared to the user, the SAS token for the sharing.
    :param config: an optional instance of the XTConfig class.
    :param max_retries: the number of times to return an Azure error before failing the associated call.

    :Example:

        >>> from store import Store
        >>> store = Store("c:/users/rfernand/.xt/xt_store")
        >>> run_names = store.get_run_names("ws1")

        '''
    
    def __init__(self, ws_root_path=None, azure_key=None, sas_token=None, subscription_id=None, resource_group=None, 
        location=None, config=None, max_retries=10, run_cache_dir=None, feedback_enabled=True, tqdm_enabled=False):
        '''This is the constructor for the XTStore class. '''

        self.run_cache_dir = run_cache_dir
        self.feedback_enabled = feedback_enabled
        self.tqdm_enabled = tqdm_enabled

        # print("store ctr: self.run_cache_dir=", self.run_cache_dir)
        # if not self.run_cache_dir:
        #     utils.user_error("must set run_cache_dir")

        if azure_key or sas_token:
            self.helper = StoreAzureBlob(ws_root_path, azure_key, sas_token, max_retries=max_retries)
            self.ws_root_path = ""

            # validate basic credentials
            try:
                self.does_workspace_exist("test")
            except BaseException as ex:
                utils.user_error("Azure Storage service credentials not set correctly" + 
                    "; use 'xt config' to correct")

        elif ws_root_path:
            self.helper = StoreFile(ws_root_path)
            self.ws_root_path = ws_root_path

        # elif subscription_id and resource_group:
        #     # AML just-in-time import (avoid heavy init costs when possible)
        #     from .store_aml import StoreAML

        #     self.helper = XTStoreAML(subscription_id, resource_group, location=location)
        #     self.ws_root_path = None

        elif config:
            store_type = config.get("core", "store-type")

            if not run_cache_dir:
                self.run_cache_dir = config.get("general", "run-cache-dir")
                root_path = config.get("core", "file-store-path")

            if store_type == "file-store":
                root_path = config.get("core", "file-store-path")
                self.helper = StoreFile(root_path)
                self.ws_root_path = root_path

            elif store_type == "azure-store":
                store_name = config.get("azure", "storage-name")
                store_key = config.get("azure", "storage-key")
                self.helper = StoreAzureBlob(store_name, store_key, max_retries=max_retries)
                self.ws_root_path = ""

            # elif store_type == "aml-store":
            #     # AML just-in-time import (avoid heavy init costs when possible)
            #     from .store_aml import StoreAML
                
            #     subscription_id = config.get("azure", "subscription-id")
            #     resource_group = config.get("azure", "resource-group")
            #     location = config.get("azure", "location")
            #     self.helper = XTStoreAML(subscription_id, resource_group, location=location)
            #     self.ws_root_path = None

            else:
                raise Exception("config file core.store must be set to 'azure-store' or 'file-store'")
        else:
            raise Exception("Must supply either ws_root_path or config parameter values")

        self.cap_stdout = None
        self.cap_stderr = None

    def _error(self, msg):
        raise Exception(f"Error - {msg}")

    # ---- WORKSPACE ----

    # internal helper
    def _ensure_workspace_exists(self, ws_name, flag_as_error=True):
        return self.helper.ensure_workspace_exists(ws_name, flag_as_error)

    def get_running_workspace(self):
        ''' returns the name of the workspace associated with the current XT run.
        '''
        return os.getenv("XT_WORKSPACE_NAME", None)

    def does_workspace_exist(self, ws_name):
        ''' returns True if the specified workspace exists in the Store; False otherwise.
        '''
        return self.helper.does_workspace_exist(ws_name)

    def create_workspace(self, ws_name, description=None):
        ''' create a new workspace using the specified name.
        '''
        self.helper.create_workspace(ws_name, description)

        # log some information
        self.log_workspace_event(ws_name, "created", {"description": description})

    def delete_workspace(self, ws_name):
        ''' delete the specified workspace, and all of the runs stored within it.
        '''
        result = self.helper.delete_workspace(ws_name)
        if result:
            # remove associated summary cache
            cache_fn = os.path.expanduser(self.run_cache_dir) + "/" + utils.RUN_SUMMARY_CACHE_FN
            cache_fn = cache_fn.replace("$ws", ws_name)
            cache_dir = os.path.dirname(cache_fn)
            print("zapping cache_dir=", cache_dir)

            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)

        return result
    
    def log_workspace_event(self, ws_name, event_name, data_dict):
        ''' log the specifed event_name and key/value pairs in the data_dict to the workspace log file.
        '''
        record_dict = {"time": _get_time(), "event": event_name, "data": data_dict}
        rd_text = json.dumps(record_dict)

        # append to workspace log file
        self.append_workspace_file(ws_name, WORKSPACE_LOG, rd_text + "\n")

    def get_workspace_names(self):
        ''' return the names of all workspaces that are currently defined in the XT Store.
        '''
        return self.helper.get_workspace_names()

    def is_legal_workspace_name(self, name):
        ''' return True if 'name' is a legal workspace name for the current XT Store.
        '''
        return self.helper.is_legal_workspace_name(name)

    # ---- WORKSPACE FILES ----

    def create_workspace_file(self, ws_name, ws_fn, text):
        ''' create a workspace file 'ws_fn" containing 'text', within the workspace 'ws_name'.
        '''
        #return self.helper.create_workspace_file(ws_name, ws_fn, text)
        wf = self.workspace_files(ws_name, use_blobs=True)
        return wf.create_file(ws_fn, text)

    def append_workspace_file(self, ws_name, ws_fn, text):
        ''' append the 'text' to the 'ws_fn' workspace file, within the workspace 'ws_name'.
        '''
        #return self.helper.append_workspace_file(ws_name, ws_fn, text)
        wf = self.workspace_files(ws_name, use_blobs=True)
        return wf.append_file(ws_fn, text)

    def read_workspace_file(self, ws_name, ws_fn):
        ''' return the text contents of the specified workspace file.'
        '''
        #return self.helper.read_workspace_file(ws_name, ws_fn)
        wf = self.workspace_files(ws_name, use_blobs=True)
        return wf.read_file(ws_fn)

    def upload_file_to_workspace(self, ws_name, ws_fn, source_fn):
        ''' upload the file 'source_fn' from the local machine to the workspace 'ws_name' as file 'ws_fn'.
        '''
        #return self.helper.upload_file_to_workspace(ws_name, ws_fn, source_fn)
        wf = self.workspace_files(ws_name, use_blobs=True)
        return wf.upload_file(wf_fn, source_n)

    def upload_files_to_workspace(self, ws_name, ws_folder, source_wildcard):
        ''' upload the local files matching 'source_wildcard' to the workspace folder 'ws_folder' within the workspace 'ws_name'.
        '''
        #return self.helper.upload_files_to_workspace(ws_name, ws_folder, source_wildcard)
        wf = self.workspace_files(ws_name, use_blobs=True)
        return wf.upload_files(ws_folder, source_wildcard)

    def download_file_from_workspace(self, ws_name, ws_fn, dest_fn):
        ''' download the file 'ws_fn' from the workspace 'ws_name' as local file 'ws_fn'.
        '''
        #dest_fn = os.path.abspath(dest_fn)      # ensure it has a directory specified
        #return self.helper.download_file_from_workspace(ws_name, ws_fn, dest_fn)
        wf = self.workspace_files(ws_name, use_blobs=True)
        return wf.download_file(ws_fn, dest_fn)

    def download_files_from_workspace(self, ws_name, ws_wildcard, dest_folder):
        ''' download the workspace files matching 'ws_wildcard' to the local folder 'dest_folder'.
        '''
        #return self.helper.download_files_from_workspace(ws_name, ws_wildcard, dest_folder)
        wf = self.workspace_files(ws_name, use_blobs=True)
        return wf.download_files(ws_wildcard, dest_folder)

    def get_workspace_filenames(self, ws_name, ws_wildcard=None):
        ''' return the name of all workspace files matching 'ws_wildcard' in the workspace 'ws_name'.
        '''
        #return self.helper.get_workspace_filenames(ws_name, ws_wildcard)    
        wf = self.workspace_files(ws_name, use_blobs=True)
        return wf.get_filenames(ws_wildcard)
        
    def delete_workspace_files(self, ws_name, ws_wildcard):
        ''' return the workspace files matching 'ws_wildcard' from the workspace 'ws_name'.
        '''
        #return self.helper.delete_workspace_files(ws_name, ws_wildcard)
        wf = self.workspace_files(ws_name, use_blobs=True)
        return wf.delete_files(ws_wildcard)

    def does_workspace_file_exist(self, ws_name, ws_fn):
        ''' return True if the specified workspace file exists in the workspace 'ws_name'.
        '''
        #return self.helper.does_workspace_file_exist(ws_name, ws_fn)
        wf = self.workspace_files(ws_name, use_blobs=True)
        return wf.does_file_exist(ws_fn)

    # ---- EXPERIMENT ----

    def does_experiment_exist(self, ws_name, exper_name):
        return self.helper.does_experiment_exist(ws_name, exper_name)

    def create_experiment(self, ws_name, exper_name):
        if self.does_experiment_exist(ws_name, exper_name):
            raise Exception("experiment already exists: workspace={}, experiment={}".format(ws_name, exper_name))
        return self.helper.create_experiment(ws_name, exper_name)

    def get_running_experiment(self):
        return os.getenv("XT_EXPERIMENT_NAME", None)

    def get_all_runs_grouped_by_experiment(self, ws_name):
        ''' returns a summary of all experiments runs in the workspace, grouped by their exper_name '''

        # build a hierarchical dict of experiments/runs
        exper_dict = {}
        #print("get_all_runs_grouped_by_experiment")

        # if self.does_workspace_file_exist(ws_name, utils.WORKSPACE_SUMMARY):
        #     text = self.read_workspace_file(ws_name, utils.WORKSPACE_SUMMARY)
        #     records = utils.load_json_records(text)
        records = self.get_run_summaries(ws_name)
        if records:
            # NOTE: "end" records are missing the "event_name" field

            for record in records:
                try:
                    if record["event"] in ["created", "start"]:     # "start" is legacy data (before 4/17/2019)
                        if "exper_name" in record and record["exper_name"]:
                            exper_name = record["exper_name"]
                        else:
                            exper_name = "<ungrouped>"

                        if not exper_name in exper_dict:
                            exper_dict[exper_name] = []

                        exper_dict[exper_name].append(record)
                except BaseException as ex:
                    print("get_all_runs_grouped_by_experiment: exception caught: ex=", ex)

        return exper_dict

    def get_run_names_for_experiment(self, ws_name, exper_name):
        ''' get list of all run_names that belong to the specified "exper_name" in the workspace. '''

        run_names_set = set()

        # if self.does_workspace_file_exist(ws_name, utils.WORKSPACE_SUMMARY):
        #     text = self.read_workspace_file(ws_name, utils.WORKSPACE_SUMMARY)
        #     records = utils.load_json_records(text)
        records = self.get_run_summaries(ws_name)
        if records:
            exper_name = exper_name.lower()

            for record in records:
                if "exper_name" in record and record["exper_name"]:
                    ename = record["exper_name"].lower()
                    if ename == exper_name:
                        run_names_set.add(record["run_name"])
                elif not exper_name or exper_name == "<ungrouped>":
                    run_names_set.add(record["run_name"])

        return list(run_names_set)        

    def get_experiment_names(self, ws_name):
        ''' get list of all unique logged "exper_name" in the workspace. '''

        exper_names_set = set()

        # if self.does_workspace_file_exist(ws_name, utils.WORKSPACE_SUMMARY):
        #     text = self.read_workspace_file(ws_name, utils.WORKSPACE_SUMMARY)
        #     records = utils.load_json_records(text)
        records = self.get_run_summaries(ws_name)
        if records:
            for record in records:
                if "exper_name" in record and record["exper_name"]:
                    exper_names_set.add(record["exper_name"])
                else:
                    exper_names_set.add("<ungrouped>")

        return list(exper_names_set)

    def get_run_names(self, ws_name):
        ''' get a flat list of all run_names in the workspace. '''
        return self.helper.get_run_names(ws_name)

    def append_experiment_run_name(self, ws_name, exper_name, run_name):
        self.helper.append_experiment_run_name( ws_name, exper_name, run_name)

    def get_experiment_run_names(self, ws_name, exper_name):
        return self.helper.get_experiment_run_names(ws_name, exper_name)

    # ---- EXPERIMENT FILES ----

    def create_experiment_file(self, ws_name, exper_name, exper_fn, text):
        ''' create an experiment file 'exper_fn" containing 'text'.
        '''
        ef = self.experiment_files(ws_name, exper_name, use_blobs=True)
        return ef.create_file(exper_fn, text)

    def append_experiment_file(self, ws_name, exper_name, exper_fn, text):
        ''' append 'text' to the experiment file 'exper_name'.
        '''
        ef = self.experiment_files(ws_name, exper_name, use_blobs=True)
        return ef.append_file(exper_fn, text)

    def read_experiment_file(self, ws_name, exper_name, exper_fn):
        ''' return the text contents of the experiment file 'exper_name'.
        '''
        #return self.helper.read_experiment_file(ws_name, exper_name, exper_fn)
        ef = self.experiment_files(ws_name, exper_name, use_blobs=True)
        return ef.read_file(exper_fn)

    def upload_file_to_experiment(self, ws_name, exper_name, exper_fn, source_fn):
        ''' upload the local file 'source_fn' as the experiment file 'exper_fn'.
        '''
        # return self.helper.upload_file_to_experiment(ws_name, exper_name, exper_fn, source_fn)
        ef = self.experiment_files(ws_name, exper_name, use_blobs=True)
        return ef.upload_file(exper_fn, source_fn)

    def upload_files_to_experiment(self, ws_name, exper_name, exper_folder, source_wildcard):
        ''' upload the local files specified by 'source_wildcard' to the experiment file folder 'exper_folder'.
        '''
        #return self.helper.upload_files_to_experiment(ws_name, exper_name, exper_folder, source_wildcard)
        ef = self.experiment_files(ws_name, exper_name, use_blobs=True)
        return ef.upload_files(exper_folder, source_wildcard)

    def download_file_from_experiment(self, ws_name, exper_name, exper_fn, dest_fn):
        ''' download file file 'exper_fn' to the local file 'dest_fn'.
        '''
        dest_fn = os.path.abspath(dest_fn)      # ensure it has a directory specified
        #return self.helper.download_file_from_experiment(ws_name, exper_name, exper_fn, dest_fn)
        ef = self.experiment_files(ws_name, exper_name, use_blobs=True)
        return ef.download_file(exper_fn, dest_fn)

    def download_files_from_experiment(self, ws_name, exper_name, exper_wildcard, dest_folder):
        ''' download the experiment files matching 'ws_wildcard' to the  folder 'dest_folder'.
        '''
        ef = self.experiment_files(ws_name, exper_name, use_blobs=True)
        return ef.download_files(ws_wildcard, dest_folder)

    def get_experiment_filenames(self, ws_name, exper_name, exper_wildcard=None):
        ''' return the name of all experiment files matching 'exper_wildcard'.
        '''
        ef = self.experiment_files(ws_name, exper_name, use_blobs=True)
        return ef.get_filenames(ws_wildcard)
        
    def delete_experiment_files(self, ws_name, exper_name, exper_wildcard):
        ''' delete the experiment files matching 'exper_wildcard'.
        '''
        ef = self.experiment_files(ws_name, exper_name, use_blobs=True)
        return wf.delete_files(exper_wildcard)

    def does_experiment_file_exist(self, ws_name, exper_name, exper_fn):
        ''' return True if the experiment file 'exper_fn' exists.
        '''
        #return self.helper.does_experiment_file_exist(ws_name, exper_name, exper_fn)
        ef = self.experiment_files(ws_name, exper_name, use_blobs=True)
        return ef.does_file_exist(exper_fn)
    
    # ---- RUN ----

    def get_running_run(self):
        return os.getenv("XT_RUN_NAME", None)

    def does_run_exist(self, ws_name, run_name):
        return self.helper.does_run_exist(ws_name, run_name)

    def _create_next_run_directory(self, ws_name, is_parent):
        '''
        Using the helper's "create_next_run_core" to create a unique, 
        sequentially number run directory.  Will retry several times
        before failing.  If it succeeds, it returns the new run name.
        '''
        # create a RETRY function to handle normal race conditons here
        retry_func = utils.make_retry_func(max_retries=5)

        context = Bag()
        context.response = None

        # minimize the retries done by helper (Azure blobs); we want to fail immediately and retry under
        # our own control
        old_retries = self.helper.set_retries(1)

        try:
            while True:
                try:
                    run_name = self.helper.create_next_run_core(ws_name, is_parent)
                except BaseException as ex:
                    context.exception = ex
                else:
                    # success
                    context.exception = None

                if not context.exception:
                    break

                backoff_time = retry_func(context)
                if not backoff_time:
                    raise context.exception

                time.sleep(backoff_time)
        finally:
            self.helper.set_retries(old_retries)

        return run_name

    def _create_next_child_directory(self, ws_name, parent_run_name):
        '''
        Using the helper's "create_next_run_core" to create a unique, 
        sequentially number CHILD run directory.  Will retry several times
        before failing.  If it succeeds, it returns the new run name.
        '''
        # create a RETRY function to handle normal race conditons here
        retry_func = utils.make_retry_func(max_retries=5)

        context = Bag()
        context.response = None

        # minimize the retries done by helper (Azure blobs)
        old_retries = self.helper.set_retries(1)

        try:
            while True:
                try:
                    run_name = self.helper.create_next_child_core(ws_name, parent_run_name)
                except BaseException as ex:
                    context.exception = ex
                else:
                    # success
                    context.exception = None

                if not context.exception:
                    break

                backoff_time = retry_func(context)
                if not backoff_time:
                    raise context.exception

                time.sleep(backoff_time)
        finally:
            self.helper.set_retries(old_retries)

        return run_name

    def create_single_run_summary_file(self, ws_name, run_name):
        #print("about to read run_log: ws_name=", ws_name, ", run_name=", run_name)
        records = self.get_run_log(ws_name, run_name)
        if not records:
            return False

        #print("records=", records)

        # append "CREATED" record to RUN summary log
        first = records[0]
        if first["event"] != "created":
            # old/corrupt run file
            return False
        
        dd = first["data"]
        dd["time"] = first["time"]
        dd["event"] = "created"

        # old runs don't have run_name and ws_name, so add them if needed
        if not "run_name" in dd:
            dd["run_name"] = run_name

        if not "ws_name" in dd:
            dd["ws_name"] = ws_name

        text = json.dumps(dd) + "\n"    
        self.append_run_file(ws_name, run_name, utils.RUN_SUMMARY_LOG, text)        

        ends = [record for record in records if record["event"] == "ended"]

        if len(ends):
            end = ends[0]   # end record from log
            dd = end["data"]

            hparams = self.gather_run_hyperparams(records)

            # append "END" record to RUN summary log
            end_record = {"ws_name": ws_name, "run_name": run_name, "time": end["time"], "event": "end", 
                "status": dd["status"], "exit_code": dd["exit_code"], 
                "hparams": hparams, "metrics": dd["metrics_rollup"], "restarts": 0}

            text = json.dumps(end_record) + "\n"
            self.append_run_file(ws_name, run_name, utils.RUN_SUMMARY_LOG, text)

        return True

    def gather_run_hyperparams(self, log_records):
        # get metric name/value to report
        cmd_records = [r for r in log_records if r["event"] == "cmd"]
        hp_records = [r for r in log_records if r["event"] == "hparams"]

        hparams = {}

        if len(cmd_records):
            # get last cmd record (app may have updated cmd line hp's)
            cr = cmd_records[-1]
            parts = cr["data"]["cmd"]
            ps = PartScanner(parts)
            part = ps.scan()

            # first cmd is app/python
            if part:
                hparams["app"] = part
                part = ps.scan()        # skip over app
                if hparams["app"] == "python":
                    # skip over python options
                    while part and part.startswith("-"):
                        part = ps.scan()

                    # part should be the name of a python file
                    hparams["app"] = part
                    part = ps.scan()

                # record options to app/python file
                while part and part.startswith("-"):
                    # identify name/value
                    if "=" in part:
                        key, value = part.split("=")
                        key = utils.strip_leading_dashes(key)
                        hparams[key] = value
                    else:
                        # is next part a value?
                        peek = ps.peek()
                        if peek and not peek.startswith("-") :
                            value = ps.scan()
                            part = utils.strip_leading_dashes(part)
                            hparams[part] = value
                        else:
                            hparams[part] = None

                    part = ps.scan()

        # now, allow app to overwrite/supplement with HP records
        for hp in hp_records:
            #print("hp=", hp)
            if "data" in hp:
                dd = hp["data"]
                for name, value in dd.items():
                    #print("found hp: ", name, ", value=", value)
                    # for hparams, we keep original str of value specified
                    hparams[name] = value

        #print("returning hparams=", hparams)
        return hparams

    def start_child_run(self, ws_name, parent_run_name, exper_name=None, cmd_line_args=None, all_args=None, description=None, 
            from_ip=None, from_host=None, app_name=None, repeat=None, box_name="local", job_id=None, pool=None, 
            node_index=None, username=None, aggregate_dest=None, path=None):
        '''
        This is usually called from the XT COMPUTE box, so we CANNOT get from_ip and from_computer_name from the local machine.
        '''

        child_name = self._create_next_child_directory(ws_name, parent_run_name)

        # we are called from controller, so our box_name is the name of this machine
        hostname = utils.get_hostname()

        # always log the true name of the box (since there can be multiple clients which would otherwise produce multiple "local"s)
        if box_name == "local":
            box_name = hostname

        # for cases where workspaces are deleted, renamed, etc, this gives a truely unique id for the run
        run_guid = str(uuid.uuid4())

        # if aggregate_dest == "experiment":
        #     self.append_experiment_run_name(ws_name, exper_name, child_name)
        # elif aggregate_dest == "job":
        #     self.append_job_run_name(job_id, child_name)

        dd = {"ws": ws_name, "run_name": child_name, "run_guid": run_guid, "description": description, "exper_name": exper_name, 
            "job_id": job_id, "pool": pool, "node_index": node_index,
            "from_ip": from_ip, "from_computer_name": from_host, "username": username, 
            "box_name": box_name, "app_name": app_name, "repeat": None, "path": path}

        # log "created" event for child run
        self.log_run_event(ws_name, child_name, "created", dd)

        # append "start" record to workspace summary log
        dd["time"] = _get_time()
        dd["event"] = "created"
        text = json.dumps(dd) + "\n"    

        # append to summary file in run dir
        self.append_run_file(ws_name, child_name, utils.RUN_SUMMARY_LOG, text)

        # # append to workspace-level summary file
        # try:
        #     self.append_workspace_file(ws_name, utils.WORKSPACE_SUMMARY, text)
        # except Exception as ex:
        #     print("warning: exception while appending to workspace summary file: " + str(ex))

        if cmd_line_args:
            self.log_run_event(ws_name, child_name, "cmd_line_args", {"data": cmd_line_args})  
        if all_args:
            self.log_run_event(ws_name, child_name, "all_args", {"data": all_args})
    
        # finally, add a "child_created" record to the parent
        self.log_run_event(ws_name, parent_run_name, "child_created", {"child_name": child_name})
        
        return child_name

    def start_run(self, ws_name, exper_name=None, description=None, username=None,
            box_name=None, app_name=None, repeat=None, is_parent=False, job_id=None, pool=None, node_index=None,
            aggregate_dest="none", path=None):
        '''
        This is usually called from the XT client machine (where user is running XT), so we can get from_ip and
        from_computer_name from the local machine.
        '''

        if repeat is not None:
            is_parent = True

        utils.timing("start_run: start")

        # helper uses a lock to ensure atomic operation here 
        run_name = self._create_next_run_directory(ws_name, is_parent)

        utils.timing("start_run: after create_next_run_directory")

        # log "created" event for run
        ip = utils.get_ip_address()
        hostname = utils.get_hostname()

        from_user = "zzz"

        # always log the true name of the box (since there can be multiple clients which would otherwise produce multiple "local"s)
        if box_name == "local":
            box_name = hostname

        if exper_name:
            # create the experiement, if it doesn't already exist
            if not self.does_experiment_exist(ws_name, exper_name):
                self.create_experiment(ws_name, exper_name)

        # if aggregate_dest == "experiment":
        #     self.append_experiment_run_name(ws_name, exper_name, run_name)
        # elif aggregate_dest == "job":
        #     self.append_job_run_name(job_id, run_name)

        # for cases where workspaces are deleted, renamed, etc, this gives a truely unique id for the run
        run_guid = str(uuid.uuid4())

        dd = {"ws": ws_name, "run_name": run_name, "run_guid": run_guid, "description": description, "exper_name": exper_name, 
            "job_id": job_id, "pool": pool, "node_index": node_index,
            "from_ip": ip, "from_computer_name": hostname, "username": username, 
            "box_name": box_name, "app_name": app_name, "repeat": repeat, "path": path}

        self.log_run_event(ws_name, run_name, "created", dd)

        utils.timing("start_run: after log_run_event")

        # append "start" record to workspace summary log
        dd["time"] = _get_time()
        dd["event"] = "created"
        text = json.dumps(dd) + "\n"

        # append to summary file in run dir
        self.append_run_file(ws_name, run_name, utils.RUN_SUMMARY_LOG, text)

        # # append to workspace-level summary file
        # try:
        #     self.append_workspace_file(ws_name, utils.WORKSPACE_SUMMARY, text)
        # except Exception as ex:
        #     print("warning: exception while appending to workspace summary file: " + str(ex))

        utils.timing("start_run: after append_workspace_file")

        return run_name

    def end_run(self, ws_name, run_name, status, exit_code, hparams_dict, metrics_rollup_dict, end_time=None, 
        restarts=0, aggregate_dest=None, dest_name=None):
        if not end_time:
            end_time = _get_time()

        self.log_run_event(ws_name, run_name, "ended", {"status": status, "exit_code": exit_code, \
            "metrics_rollup": metrics_rollup_dict}, event_time=end_time)

        # append "end" record to workspace summary log
        end_record = {"ws_name": ws_name, "run_name": run_name, "time": end_time, "event": "end", 
            "status": status, "exit_code": exit_code, "hparams": hparams_dict, "metrics": metrics_rollup_dict, 
            "restarts": restarts}

        text = json.dumps(end_record) + "\n"

        # append to summary file in run dir
        self.append_run_file(ws_name, run_name, utils.RUN_SUMMARY_LOG, text)

        if aggregate_dest == "experiment":
            self.append_experiment_run_name(ws_name, dest_name, run_name)
        elif aggregate_dest == "job":
            self.append_job_run_name(dest_name, run_name)

        # # append to workspace-level summary file
        # try:
        #     self.append_workspace_file(ws_name, utils.WORKSPACE_SUMMARY, text)
        # except Exception as ex:
        #     print("warning: exception while appending to workspace summary file: " + str(ex))

    def delete_run(self, ws_name, run_name):
        return self.helper.delete_run(ws_name, run_name)

    def nest_run_records(self, ws_name, run_name):
        ''' return a single record that includes the all of the run_log in the data dictionary '''
        records = self.get_run_log(ws_name, run_name)    
        last_end_time = records[-1]["time"]

        log_record = {"run_name": run_name, "log": records}
        text = json.dumps(log_record) + "\n"
        #print("\ntext=", text)
        return text, last_end_time

    def rollup_and_end_run(self, ws_name, run_name, aggregate_dest, dest_name, status, exit_code, metric_rollup_dict, 
        use_last_end_time=False):

        # write run to ALLRUNS file
        if aggregate_dest and aggregate_dest != "none":
            # convert entire run log to a single nested record
            text, last_end_time = self.nest_run_records(ws_name, run_name)

            # append nested record to the specified all_runs file
            if dest_name:
                if aggregate_dest == "experiment":
                    self.append_experiment_file(ws_name, dest_name, utils.ALL_RUNS_FN, text)
                elif aggregate_dest == "job":
                    self.append_job_file(dest_name, utils.ALL_RUNS_FN, text)

        if use_last_end_time:
            end_time = last_end_time
        else:
            end_time = _get_time()

        # LOG END RUN
        log_records = self.get_run_log(ws_name, run_name)

        hparams = self._roll_up_hparams(log_records) 
        metrics = self.rollup_metrics_from_records(log_records, metric_rollup_dict) 
        restarts = len([rr["event"] for rr in log_records if rr["event"] == "restarted"])

        self.end_run(ws_name, run_name, status, exit_code, hparams, metrics, restarts=restarts, 
            end_time=end_time, aggregate_dest=aggregate_dest, dest_name=dest_name)

    def _roll_up_hparams(self, log_records):
        hparams_dict = {}

        for record in log_records:
            if record["event"] == "hparams":
                dd = record["data"]
                for key,value in dd.items():
                    hparams_dict[key] = value
                    
        return hparams_dict

    def rollup_metrics_from_records(self, log_records, metric_rollup_dict):
        metrics_records = [record for record in log_records if record["event"] == "metrics"]
        gather_dict = {}
        rollup_dict = {}

        for mr in metrics_records:
            if "data" in mr:
                dd = mr["data"]
                for key, value in dd.items():
                    if value:
                        if not key in gather_dict:
                            gather_dict[key] = []

                        try:
                            # ---- some strings may be invalid ints/floats - just ignore them for now
                            if isinstance(value, str):
                                #print("string found: key=", key, ", value=", value)  # , ", ex=", ex)
                                if "." in value or value == 'nan':
                                    value = float(value)
                                else:
                                    value = int(value)

                        except BaseException as ex:
                            #print("exception found: key=", key, ", value=", value, ", ex=", ex)
                            pass

                        #print("rollup gather: key={}, value={}".format(key, value))
                        gather_dict[key].append(value)

        for key, values in gather_dict.items():
            if key in metric_rollup_dict:
                mr = metric_rollup_dict[key]["roll-up"]
            else:
                mr = "max"

            # allow for string or None metrics

            try:
                if mr == "first":
                    value = values[0]
                elif mr == "last":
                    value = values[-1]
                elif mr == "min":
                    value = min(values)
                elif mr == "max":
                    value = max(values)
                elif mr == "mean":
                    value = np.mean(values)
            except:
                # when above fails, just use 'last' 
                value = values[-1]

            rollup_dict[key] = value
            #print("rollup: values=", values)
            #print("rollup: key=", key, ", value=", value, ", type(value)=", type(value))
        
        return rollup_dict

    def copy_run(self, ws_name, run_name, ws_name2, run_name2):
        return self.helper.copy_run(ws_name, run_name, ws_name2, run_name2)

    def get_run_log(self, ws_name, run_name):
        return self.helper.get_run_log(ws_name, run_name)

    def log_run_event(self, ws_name, run_name, event_name, data_dict=None, description=None, event_time=None):
        if not event_time:
            event_time = _get_time()

        if data_dict and not isinstance(data_dict, dict):   
            raise Exception("data_dict argument is not a dict: " + str(data_dict))
        record_dict = {"time": event_time, "event": event_name, "data": data_dict, "description": description}
        #print("record_dict=", record_dict)

        rd_text = json.dumps(record_dict)
        # append to run log file
        self.append_run_file(ws_name, run_name, RUN_LOG, rd_text + "\n")

    def wrapup_run(self, ws_name, run_name, aggregate_dest, dest_name, status, exit_code, metric_rollup_dict, rundir, 
        after_files_list, log_events=True, capture_files=True):

        if log_events:  
            # LOG "ENDED" to run_log, APPEND TO ALLRUNS
            self.rollup_and_end_run(ws_name, run_name, aggregate_dest, dest_name, status, exit_code, metric_rollup_dict)

        if rundir and capture_files:
            # CAPTURE OUTPUT FILES
            started = time.time()
            copied_files = []

            for output_files in after_files_list:
                from_path = os.path.dirname(output_files)
                to_path = "after/" + from_path if from_path else "after" 
                output_files = os.path.abspath(utils.path_join(rundir, output_files))
                #print("\nprocessing output_files=", output_files, ", from_path=", from_path, ", to_path=", to_path)

                copied = self.upload_files_to_run(ws_name, run_name, to_path, output_files)
                #print("copied=", copied)
                copied_files += copied

            elapsed = time.time() - started
            self.log_run_event(ws_name, run_name, "capture_after", {"elapsed": elapsed, "count": len(copied_files)})

    def copy_run_files_to_run(self, ws_name, from_run, run_wildcard, to_run, to_path):
        return self.helper.copy_run_files_to_run(ws_name, from_run, run_wildcard, to_run, to_path)

    #---- CLIENT CACHING ----

    def get_run_summaries(self, ws_name):
        # PERF-critical function 
        summary_dict = {}     # key examples: run23_start, run46_end, etc.
        utils.timing("get_run_summaries: starting")

        # first, get list of all runs in workspace
        updates_needed = self.helper.get_run_names(ws_name)
        #print("orig updates_needed=", updates_needed)
        utils.timing("get_run_summaries: after get_run_names, updates_needed={}".format(len(updates_needed)))

        # use records in local cache to reduce needed updates
        #cache_fn = os.path.expanduser(utils.RUN_SUMMARY_CACHE_FN)
        if not self.run_cache_dir:
            print("'run-cache-dir' not set; cache not used")
        else:
            cache_fn = os.path.expanduser(self.run_cache_dir) + "/" + utils.RUN_SUMMARY_CACHE_FN
            cache_fn = cache_fn.replace("$ws", ws_name)
            cache_count = 0
            utils.timing("get_run_summaries: cache_fn=" + cache_fn)

            try:
                if os.path.exists(cache_fn):
                    with open(cache_fn, "r") as infile:
                        text = infile.read()
                
                    # add records to summary_dict
                    records = json.loads(text)
                    #print("len(records)=", len(records))

                    cache_count = len(records)

                    for rec in records:
                        key = rec["run_name"] + "-" + rec["event"]
                        summary_dict[key] = rec

                    #print("processed {} records from cache summary file".format(len(records)))
                    utils.timing("get_run_summaries: after processing cache file")
            except BaseException as ex:
                print("** exception during read of cache; cachefn={}, ex={}".format(cache_fn, ex))

        # remove entries from updates_needed where we find an 'end' record
        for key, value in summary_dict.items():
            #print("key=", key)
            if key.endswith("-end"):
                run_name = value["run_name"]
                if run_name in updates_needed:
                    updates_needed.remove(run_name)

        if self.feedback_enabled:
            end = "\n" if self.tqdm_enabled else ""
            print("read {} runs from cache; now reading {} runs from store: ".format(cache_count, len(updates_needed)), end="")

        # now, read any other runs in workspace and add them to summary_records
        read_count = 0
        added_count = 0
        tq = None

        if updates_needed:
            if self.feedback_enabled:
                if self.tqdm_enabled:
                    from tqdm import tqdm
                    #print("downloading files...")
                    tq = tqdm(ncols=100, total=len(updates_needed)) 

            try:
                for run_name in updates_needed:
                    # TEMP TEMP TEMP (repair badly constructed summary files)
                    # if self.does_run_file_exist(ws_name, run_name, utils.RUN_SUMMARY_LOG):
                    #     self.delete_run_files(ws_name, run_name, utils.RUN_SUMMARY_LOG)

                    if not self.does_run_file_exist(ws_name, run_name, utils.RUN_SUMMARY_LOG):
                        # legacy run files (created before v.80, 8/1/2019)
                        # take a perf hit and create the summary file just this once (will persist in run dir of store)
                        print("  upgrading legacy run: {}/{}".format(ws_name, run_name))
                        upgraded = self.create_single_run_summary_file(ws_name, run_name)
                        if not upgraded:
                            continue

                    text = self.read_run_file(ws_name, run_name, utils.RUN_SUMMARY_LOG)
                    run_records = utils.load_json_records(text)
                    read_count += 1

                    # merge with summary_dict
                    for rr in run_records:
                        #print("rr=", rr)
                        key = run_name + "-" + rr["event"]
                        if not key in summary_dict:
                            summary_dict[key] = rr
                            added_count += 1

                    if tq:
                        tq.update()
                    elif self.feedback_enabled:
                        print(".", end="")
                        sys.stdout.flush()
            finally:
                if tq:
                    tq.close()
                elif self.feedback_enabled:
                    print()

        summary_records = list(summary_dict.values())
        utils.timing("get_run_summaries: after reading {} run_summary files, added_count={}".format(read_count, added_count))

        # finally, update the summary records file
        if added_count:
            text = json.dumps(summary_records)
            utils.ensure_dir_exists(file=cache_fn)

            try:
                with open(cache_fn, "w") as outfile:
                    outfile.write(text)
            except BaseException as ex:
                print("** exception during write of cache; cachefn={}, ex={}".format(cache_fn, ex))
            
            utils.timing("get_run_summaries: after updating cache: " + cache_fn)

        return summary_records

    def get_all_runs(self, aggregator_dest, ws_name, job_or_exper_name):
        # PERF-critical function 
        allrun_dict = {}     # key examples: run23, run46, etc.
        utils.timing("get_all_runs: starting")

        # first, get list of all runs in aggregator
        if aggregator_dest == "job":
            updates_needed = self.get_job_run_names(job_or_exper_name)
        elif aggregator_dest == "experiment":
            updates_needed = self.get_experiment_run_names(ws_name, job_or_exper_name)
        elif aggregator_dest is None or aggregator_dest == "none":
            utils.user_error("[hp-search] 'aggregator-dest' property must be set to 'job' or 'experiment' (in xt config file)")
        else:
            utils.user_error("unrecognized [hp-search] aggregator-dest value: ", aggregator_dest)

        #print("orig updates_needed=", updates_needed)
        utils.timing("get_all_runs: after get_xxx_run_names")

        # use records in local cache to reduce needed updates
        #cache_fn = os.path.expanduser(utils.ALL_RUNS_CACHE_FN)
        cache_count = 0

        if not self.run_cache_dir:
            print("'run-cache-dir' not set; cache not used")
            cache_fn = None
        else:
            cache_fn = os.path.expanduser(self.run_cache_dir) + "/" + utils.ALL_RUNS_CACHE_FN

            if aggregator_dest == "job":
                cache_fn = cache_fn.replace("$aggregator", job_or_exper_name)
            else:
                cache_fn = cache_fn.replace("$aggregator", ws_name + "/" + job_or_exper_name)

            try:
                if os.path.exists(cache_fn):
                    with open(cache_fn, "r") as infile:
                        text = infile.read()
                
                    # add records to allrun_dict
                    records = json.loads(text)
                    cache_count = len(records)

                    for rec in records:
                        key = rec["run_name"] 
                        allrun_dict[key] = rec

                    #print("processed {} records from cache allruns file".format(len(records)))
                    utils.timing("get_all_runs: after processing cache file")
            except BaseException as ex:
                print("** exception during read of cache; cachefn={}, ex={}".format(cache_fn, ex))

        # remove entries from updates_needed where we find an 'end' record
        for run_name, value in allrun_dict.items():
            #print("key=", run_name)
            if run_name in updates_needed:
                updates_needed.remove(run_name)

        if self.feedback_enabled:
            end = "\n" if self.tqdm_enabled else ""
            print("read {} runs from cache; now reading {} runs from store: ".format(cache_count, len(updates_needed)), end="")

        # now, read any other runs in workspace and add them to allrun_dict
        added_records = False
        read_count = 0
        tq = None

        if updates_needed:
            if self.feedback_enabled and self.tqdm_enabled:
                from tqdm import tqdm
                #print("downloading files...")
                tq = tqdm(ncols=100, total=len(updates_needed)) 

            try:
                for run_name in updates_needed:
                    if self.does_run_file_exist(ws_name, run_name, utils.RUN_LOG):
                        records = self.helper.get_run_log(ws_name, run_name)
                        read_count += 1

                        # only include this run if it has ended
                        ends = [record for record in records if record["event"] == "ended"]
                        if len(ends) > 0:
                            # aggregate all run log records from this run into a single record
                            log_record = {"run_name": run_name, "log": records}

                            # merge into allrun_dict
                            allrun_dict[run_name] = log_record
                            added_records = True
                    if tq:
                        tq.update()
                    elif self.feedback_enabled:
                        print(".", end="")
                        sys.stdout.flush()
                        
            finally:
                if tq:
                    tq.close()
                elif self.feedback_enabled:
                    print()
        
        allrun_records = list(allrun_dict.values())
        utils.timing("get_all_runs: after reading {} allrun_dict files".format(read_count))

        # finally, update the allruns cache file
        if added_records and cache_fn:
            text = json.dumps(allrun_records)
            
            try:
                utils.ensure_dir_exists(file=cache_fn)
                with open(cache_fn, "w") as outfile:
                    outfile.write(text)
            except BaseException as ex:
                print("** exception during write of cache; cachefn={}, ex={}".format(cache_fn, ex))

        utils.timing("get_all_runs: after updating cache")
        return allrun_records

    # ---- RUN FILES ----

    def create_run_file(self, ws_name, run_name, run_fn, text):
        '''create the specified run file 'run_fn' from the specified 'text'.
        '''
        #return self.helper.create_run_file(ws_name, run_name, run_fn, text)
        rf = self.run_files(ws_name, run_name, use_blobs=True)
        return rf.create_file(run_fn, text)

    def append_run_file(self, ws_name, run_name, run_fn, text):
        '''append 'text' to the run file 'run_fn'.
        '''
        #return self.helper.append_run_file(ws_name, run_name, run_fn, text)
        rf = self.run_files(ws_name, run_name, use_blobs=True)
        return rf.append_file(run_fn, text)

    def read_run_file(self, ws_name, run_name, run_fn):
        '''return the contents of the run file 'run_fn'.
        '''
        #return self.helper.read_run_file(ws_name, run_name, run_fn)
        rf = self.run_files(ws_name, run_name, use_blobs=True)
        return rf.read_file(run_fn)

    def upload_file_to_run(self, ws_name, run_name, run_fn, source_fn):
        '''upload the local file 'source_fn' as the run file 'run_fn'.
        '''
        #return self.helper.upload_file_to_run(ws_name, run_name, run_fn, source_fn)
        rf = self.run_files(ws_name, run_name, use_blobs=True)
        return rf.upload_file(run_fn, source_fn)

    def upload_files_to_run(self, ws_name, run_name, run_folder, source_wildcard, exclude_dirs_and_files=[]):
        '''upload the local files specified by 'source_wildcard' to the run folder 'run_folder'.
        '''
        #return self.helper.upload_files_to_run(ws_name, run_name, run_folder, source_wildcard, exclude_dirs)
        rf = self.run_files(ws_name, run_name, use_blobs=True)
        return rf.upload_files(run_folder, source_wildcard, exclude_dirs_and_files=exclude_dirs_and_files)

    def download_file_from_run(self, ws_name, run_name, run_fn, dest_fn):
        '''download the run file 'run_fn' to the local file 'dest_fn'.
        '''
        dest_fn = os.path.abspath(dest_fn)      # ensure it has a directory specified
        #return self.helper.download_file_from_run(ws_name, run_name, run_fn, dest_fn)
        rf = self.run_files(ws_name, run_name, use_blobs=True)
        return rf.download_file(run_fn, dest_fn)

    def download_files_from_run(self, ws_name, run_name, run_wildcard, dest_folder):
        '''download the run files specified by 'run_wildcard' to the local folder 'dest_folder'.
        '''
        #return self.helper.download_files_from_run(ws_name, run_name, run_wildcard, dest_folder)
        rf = self.run_files(ws_name, run_name, use_blobs=True)
        return rf.download_files(run_wildcard, dest_folder)

    def get_run_filenames(self, ws_name, run_name, run_wildcard=None):
        '''return the names of the run files specified by 'run_wildcard'.
        '''
        #return self.helper.get_run_filenames(ws_name, run_name, run_wildcard)    
        rf = self.run_files(ws_name, run_name, use_blobs=True)
        return rf.get_filenames(run_wildcard)
        
    def delete_run_files(self, ws_name, run_name, run_wildcard):
        '''delete the run files specified by 'run_wildcard'.
        '''
        #return self.helper.delete_run_files(ws_name, run_name, run_wildcard)
        rf = self.run_files(ws_name, run_name, use_blobs=True)
        return rf.delete_files(run_wildcard)

    def does_run_file_exist(self, ws_name, run_name, run_fn):
        '''return True if the specified run file 'run_fn' exists.
        '''
        #return self.helper.does_run_file_exist(ws_name, run_name, run_fn)
        rf = self.run_files(ws_name, run_name, use_blobs=True)
        return rf.does_file_exist(run_fn)

    #---- JOBS ----

    def _create_next_job_file(self):
        '''
        Using the helper's "create_next_job_core" to create a unique, 
        sequentially numbered job file.  Will retry several times
        before failing.  If it succeeds, it returns the new job name.
        '''
        # create a RETRY function to handle normal race conditons here
        retry_func = utils.make_retry_func(max_retries=5)

        context = Bag()
        context.response = None

        # minimize the retries done by helper (Azure blobs); we want to fail immediately and retry under
        # our own control
        old_retries = self.helper.set_retries(1)

        try:
            while True:
                try:
                    job_name = self.helper.create_next_job_core()
                except BaseException as ex:
                    context.exception = ex
                else:
                    # success
                    context.exception = None

                if not context.exception:
                    break

                backoff_time = retry_func(context)
                if not backoff_time:
                    raise context.exception

                time.sleep(backoff_time)
        finally:
            self.helper.set_retries(old_retries)

        return job_name

    def create_job(self):

        # helper uses a lock to ensure atomic operation here 
        job_name = self._create_next_job_file()
        return job_name

    def read_job_info_file(self, job_name):
        return self.helper.read_job_info_file(job_name)

    def write_job_info_file(self, job_name, text):
        self.helper.write_job_info_file(job_name, text)
    
    def log_job_info(self, job_id, pool_info, runs_by_box):
        dd = {"job_id": job_id, "pool_info": pool_info, "runs_by_box": runs_by_box}
        text = json.dumps(dd)
        self.write_job_info_file(job_id, text)

    def log_job_event(self, job_id, event_name, data_dict=None, description=None, event_time=None):
        if not event_time:
            event_time = _get_time()

        if data_dict and not isinstance(data_dict, dict):   
            raise Exception("data_dict argument is not a dict: " + str(data_dict))
        record_dict = {"time": event_time, "event": event_name, "data": data_dict, "description": description}
        #print("record_dict=", record_dict)

        rd_text = json.dumps(record_dict)
        # append to run log file
        self.append_job_file(job_id, utils.JOB_LOG, rd_text + "\n")

    def get_job_names(self):
        return self.helper.get_job_names()

    #---- JOB FILES ----

    def create_job_file(self, job_name, job_path, text):
        '''create a job file specified by 'job_path' from the text 'text'.
        '''
        #self.helper.create_job_file(job_name, job_path, text)
        jf = self.job_files(job_name, use_blobs=True)
        return jf.create_file(job_path, text)

    def append_job_file(self, job_name, job_path, text):
        '''append text 'text' to the job file 'job_path'.
        '''
        #self.helper.append_job_file(job_name, job_path, text)
        jf = self.job_files(job_name, use_blobs=True)
        return jf.append_file(job_path, text)

    def read_job_file(self, job_name, job_path):
        '''return the contexts of the job file 'job_path'.
        '''
        #return self.helper.read_job_file(job_name, job_path)
        jf = self.job_files(job_name, use_blobs=True)
        return jf.read_file(job_path)

    def upload_file_to_job(self, job_name, fn_job, fn_source):
        '''upload the local file 'fn_source' as the job file 'fn_job'.
        '''
        #return self.helper.upload_file_to_job(job_name, job_folder, fn_source)
        jf = self.job_files(job_name, use_blobs=True)
        return jf.upload_file(fn_job, fn_source)

    def upload_files_to_job(self, job_name, job_folder, source_wildcard, recursive=False, exclude_dirs_and_files=[]):
        '''upload the local files specified by 'source_wildcard' to the job folder 'job_folder'.
        '''
        #return self.helper.upload_files_to_job(job_name, job_folder, source_wildcard)
        jf = self.job_files(job_name, use_blobs=True)
        return jf.upload_files(job_folder, source_wildcard, recursive=recursive, exclude_dirs_and_files=exclude_dirs_and_files)

    def download_file_from_job(self, job_name, job_fn, dest_fn):
        '''download the job file 'job_fn' to the local file 'dest_fn'.
        '''
        #return self.helper.download_file_from_job(job_name, job_fn, dest_fn)
        jf = self.job_files(job_name, use_blobs=True)
        return jf.download_file(job_fn, dest_fn)

    def download_files_from_job(self, job_name, job_wildcard, dest_folder):
        #return self.helper.download_files_from_job(job_name, job_wildcard, dest_folder)
        jf = self.job_files(job_name, use_blobs=True)
        return jf.download_files(job_wildcard, dest_folder)

    def get_job_filenames(self, job_name, job_wildcard=None, full_paths=False):
        '''return the names of the job files specified by 'job_wildcard'.
        '''
        #return self.helper.get_run_filenames(ws_name, run_name, run_wildcard)    
        jf = self.job_files(job_name, use_blobs=True)
        return jf.get_filenames(job_wildcard, full_paths=full_paths)

    def delete_job_files(self, job_name, job_wildcard):
        '''delete the job files specified by 'job_wildcard'.
        '''
        #return self.helper.delete_run_files(ws_name, run_name, run_wildcard)
        jf = self.job_files(job_name, use_blobs=True)
        return jf.delete_files(job_wildcard)

    def does_job_file_exist(self, job_name, job_path):
        '''return True if the job file 'job_path' exists.
        '''
        #return self.helper.does_job_file_exist(job_name, job_path)
        jf = self.job_files(job_name, use_blobs=True)
        return jf.does_file_exist(job_path)

    def append_job_run_name(self, job_name, run_name):
        return self.helper.append_job_run_name(job_name, run_name)

    def get_job_run_names(self, job_name):
        return self.helper.get_job_run_names(job_name)

    # ---- DIRECT ACCESS ----
    
    def list_files(self, ws, path, subdirs=0):
        if not subdirs:
            subdirs = 0

        if path and path.startswith("store:"):
            path = path[6:]
        return self.helper.list_files(ws, path, subdirs)

    def read_store_file(self, ws, path):
        return self.helper.read_store_file(ws, path)

    # ---- CAPTURE OUTPUT ----

    def capture_stdout(self, fn=RUN_STDOUT):
        self.cap_stdout = StreamCapture(sys.stdout, fn)
        sys.stdout = self.cap_stdout

    def capture_stderr(self, fn=RUN_STDERR):
        self.cap_stderr = StreamCapture(sys.stderr, fn)
        sys.stderr = self.cap_stderr

    def release_stdout(self):
        if self.cap_stdout:
            sys.stdout = self.cap_stdout.close()

    def release_stderr(self):
        if self.cap_stderr:
            sys.stderr = self.cap_stderr.close()

    # ---- FILES OBJECTS ----

    def workspace_files(self, ws_name, use_blobs=False):
        return self.helper.workspace_files(ws_name, use_blobs)

    def run_files(self, ws_name, run_name, use_blobs=False):
        return self.helper.run_files(ws_name, run_name, use_blobs)

    def experiment_files(self, ws_name, exper_name, use_blobs=False):
        return self.helper.experiment_files(ws_name, exper_name, use_blobs)

    def job_files(self, job_name, use_blobs=False):
        return self.helper.job_files(job_name, use_blobs)

# sample code for path objects
#   wp = store.WorkspaceFiles(ws_name="ws1")  
#   wp.create_file("test.txt", "this is test.txt contents")




