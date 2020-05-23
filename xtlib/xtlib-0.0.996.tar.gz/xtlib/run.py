# runner.py - simple API for ML apps to log info and get info related to current run
import os
import json

from .store import Store
from . import utils

FN_CHECKPOINT_FILE = "checkpoints/file.dat"
FN_CHECKPOINT_DICT = "checkpoints/dict_cp.json"
FN_CHECKPOINT_WILD = "checkpoints/*"

class Run():

    def __init__(self, xt_config=None, store=None):

        store_path = os.getenv("XT_STORE_PATH")
        store_key = os.getenv("XT_STORE_KEY")
        store_type = os.getenv("XT_STORE_TYPE")

        run_cache_dir = None
        if xt_config:
            run_cache_dir = xt_config.get("general", "run-cache-dir")

        if store:
            self.store = store
        elif store_type == "azure-store" and store_path and store_key:
            self.store = Store(store_path, store_key, run_cache_dir=run_cache_dir)
        elif store_type == "file-store" and store_path:
            self.store = Store(store_path, run_cache_dir=run_cache_dir)
        else:
            self.store = None

        if self.store:
            self.ws_name = self.store.get_running_workspace()
            self.run_name = self.store.get_running_run()
            self.exper_name = self.store.get_running_experiment()
        else:
            self.ws_name = None
            self.run_name = None
            self.exper_name = None

        self.resume_name = os.getenv("XT_RESUME_NAME")
        
        # distributed training support
        self.rank = None
        self.world_size = None
        self.master_ip = None
        self.master_port = None

        # print("XTRunLog: store_type={}, store_path={}, store={}, ws_name={}, run_name={}, version={}".   \
        #    format(store_type, store_path, self.store, self.ws_name, self.run_name, utils.BUILD))

    def get_store(self):
        return self.store

    def log_hparam(self, name, value, description=None):
        if self.store:
            self.store.log_run_event(self.ws_name, self.run_name, "hparams", {name: value}, description=description)

    def log_hparams(self, data_dict, description=None):
        #print("log_hparam, self.store=", self.store)
        if self.store:
            self.store.log_run_event(self.ws_name, self.run_name, "hparams", data_dict, description=description)

    def log_metric(self, name, value, description=None):
        if self.store:
            self.store.log_run_event(self.ws_name, self.run_name, "metrics", {name: value}, description=description)

    def log_metrics(self, data_dict, description=None):
        if self.store:
            self.store.log_run_event(self.ws_name, self.run_name, "metrics", data_dict, description=description)

    def log_event(self, event_name, data_dict, description=None):
        if self.store:
            self.store.log_run_event(self.ws_name, self.run_name, event_name, data_dict, description=description)

    def is_resuming(self):
        # return a bool using not not
        return not not self.resume_name 

    def set_checkpoint(self, dict_cp, fn_cp=None):
        if self.store:
            if fn_cp:
                #print("uploading checkpoint file: ws={}, run={}, file={}".format(self.ws_name, self.run_name, FN_CHECKPOINT_FILE))
                self.store.upload_file_to_run(self.ws_name, self.run_name, FN_CHECKPOINT_FILE, fn_cp)
            text = json.dumps(dict_cp)
            #print("uploading checkpoint dict: ws={}, run={}, file={}".format(self.ws_name, self.run_name, FN_CHECKPOINT_DICT))
            self.store.create_run_file(self.ws_name, self.run_name, FN_CHECKPOINT_DICT, text)

            # also log the checkpoint
            self.store.log_run_event(self.ws_name, self.run_name, "set_checkpoint", dict_cp)
            return True
        return False

    def clear_checkpoint(self):
        if self.store:
            self.store.delete_run_files(self.ws_name, self.run_name, FN_CHECKPOINT_WILD)
            self.store.log_run_event(self.ws_name, self.run_name, "clear_checkpoint", dict_cp)
            return True
        return False

    def get_checkpoint(self, fn_cp_dest=None):
        dict_cp = None

        if self.store and self.is_resuming():
            if self.store.does_run_file_exist(self.ws_name, self.resume_name, FN_CHECKPOINT_DICT):
                if fn_cp_dest:
                    #print("downloading checkpoint file: ws={}, run={}, file={}".format(self.ws_name, self.resume_name, FN_CHECKPOINT_FILE))
                    self.store.download_file_from_run(self.ws_name, self.resume_name, FN_CHECKPOINT_FILE, fn_cp_dest)
                #print("downloading checkpoint dict: ws={}, run={}, file={}".format(self.ws_name, self.resume_name, FN_CHECKPOINT_DICT))
                text = self.store.read_run_file(self.ws_name, self.resume_name, FN_CHECKPOINT_DICT)
                dict_cp = json.loads(text)
                # log that we retreived the checkpoint
                self.store.log_run_event(self.ws_name, self.run_name, "get_checkpoint", dict_cp)

        return dict_cp
