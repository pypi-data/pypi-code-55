# store_file.py - implements xt_store support for file-based storge (local machine, server)

import os
import re
import shutil
import json
import time

from . import utils

class StoreFile():
    def __init__(self, store_root_path):
        store_root_path = os.path.expanduser(store_root_path)
        self.store_root_path = store_root_path
        #print("store_root_path=", store_root_path)

        # create root_path now, if needed
        if not os.path.exists(store_root_path):
            os.makedirs(store_root_path)

    # ---- INTERNAL HELPERS ----
    def _error(self, msg):
        raise Exception(f"_error - {msg}")

    def _create_file(self, fn, text):
        utils.ensure_dir_exists(file=fn)
        with open(fn, "w") as afile:
            afile.write(text)

    def _append_file(self, fn, text):
        with open(fn, "a+") as afile:
            afile.write(text)

    def _read_file(self, fn):
        with open(fn, "r") as afile:
            text = afile.read()
        return text
        
    def _copy_file(self, source_fn, dest_fn):
        # ensure dest directory exists
        dd = os.path.dirname(dest_fn)
        if not os.path.exists(dd):
            os.makedirs(dd)

        shutil.copyfile(source_fn, dest_fn)

    def _copy_files(self, source_wildcard, dest_folder, recursive=False, exclude_dirs_and_files=[]):
        copied_files = []
        #print("_copy_files: source_wildcard=", source_wildcard, ", dest_folder=", dest_folder)
        utils.ensure_dir_exists(dest_folder)

        # handle special "**" for recursive copy
        if source_wildcard == "**":
            recursive = True
            source_wildcard = "*"

        for source_fn in utils.glob(source_wildcard):
            source_name = os.path.basename(source_fn)
            if source_name in exclude_dirs_and_files:
                # skip over any excluded file or directory
                continue

            if os.path.isfile(source_fn):
                dest_fn = dest_folder + "/" + source_name
                shutil.copyfile(source_fn, dest_fn)
                copied_files.append(source_fn)
            elif os.path.isdir(source_fn) and recursive:
                # copy subdir
                copied = self._copy_files(source_fn + "/*", dest_folder + "/" + source_name, exclude_dirs_and_files)
                copied_files = copied_files + copied

        #print("copied_files=", copied_files)
        return copied_files

    def _delete_files(self, file_wildcard):
        delete_count = 0

        for fn in utils.glob(file_wildcard):
            os.remove(fn)
            delete_count += 1

        return delete_count

    def _get_jobs_dir(self):
        ''' return the path to the "jobs" dir in the info container'''
        path = self.store_root_path + "/" + utils.INFO_CONTAINER + "/" + utils.JOBS_DIR
        return path

    def _get_job_path(self, job_name):
        ''' return the path to the jobs/jobxxx'''
        path =  self._get_jobs_dir() + "/" + job_name
        return path

    def _get_job_file_path(self, job_name, blob_path):
        fn_job = self._get_jobs_dir() + "/" + job_name + "/" + blob_path
        return fn_job

    def _get_workspace_path(self, ws_name):
        ''' return the path to the workspace's MAIN directory'''
        path = self.store_root_path + "/" + ws_name
        return path

    def _get_workspace_path_fn(self, ws_name, fn=None):
        ''' return the path to a file in the workspace's FILE directory  '''
        path = self.store_root_path + "/" + ws_name + "/" + utils.WORKSPACE_DIR 
        if fn:
            path += "/" + fn
        return path

    def _get_exper_path(self, ws_name, exper_name):
        ''' return a path to the specified experiments MAIN directory'''
        path = self.store_root_path + "/" + ws_name + "/" + utils.EXPERIMENTS_DIR + "/" + exper_name
        #print("_get_exper_path: root=",  self.store_root_path, ", path=", path)
        return path

    def _get_exper_path_fn(self, ws_name, exper_name, fn=None):
        ''' return a path to the specified experiments MAIN directory'''
        path = self.store_root_path + "/" + ws_name + "/" + utils.EXPERIMENTS_DIR + "/" + exper_name
        if fn:
            path += "/" + fn
        #print("_get_exper_path: root=",  self.store_root_path, ", path=", path)
        return path

    def _get_run_path(self, ws_name, run_name):
        ''' return a path to the specified run's MAIN directory'''
        path = self.store_root_path + "/" + ws_name + "/" + utils.RUNS_DIR + "/" + run_name
        #print("_get_run_path: root=",  self.store_root_path, ", path=", path)
        return path

    def _get_run_path_fn(self, ws_name, run_name, fnx):
        ''' return the path to a file in the run's FILE directory '''
        path = self._get_run_path(ws_name, run_name)
        #print("_get_run_path_fn: path=", path)
        if fnx:
            path += "/" + fnx
        return path

    def _get_filesnames(self, wild_path, relative_paths=False):
        if os.path.isdir(wild_path):
            wild_path += "/*"
        #print("wild_path=", wild_path)

        file_names = utils.glob(wild_path)
        file_names = [fn for fn in file_names if os.path.isfile(fn)]

        if relative_paths:
            file_names = [os.path.basename(fn) for fn in file_names]

        return file_names

    def _list_files(self, wild_path, recursive=False):

        root = utils.fix_slashes(self.store_root_path)

        dd = {"store_name": "XT File Store ({})".format(root)}
        root_len = len(root)

        folders = []
        dd["folders"] = folders

        folder, full_dir_names = self._get_folder_files(wild_path)
        folders.append(folder)

        if recursive:
            dirs_to_list = list(full_dir_names)
            while dirs_to_list:
                dir_path = dirs_to_list.pop(0)
                folder, full_dir_names = self._get_folder_files(dir_path)

                folders.append(folder)
                dirs_to_list = full_dir_names + dirs_to_list

        return dd

    def _get_folder_files(self, wild_path):
        wp = os.path.basename(wild_path)

        # create a new folder
        folder = {}
        base_len = len(self.store_root_path)
        #print("wild_path=", wild_path)

        name = wild_path[base_len:]
        if name == "//":
            name = "/"
        folder["folder_name"] = name
        
        if os.path.isdir(wild_path):
            wild_path += "/*"
        #print("wild_path=", wild_path)

        all_names = utils.glob(wild_path)
        file_names = [fn for fn in all_names if os.path.isfile(fn)]
        full_dir_names = [fn for fn in all_names if not os.path.isfile(fn)]
        dir_names = [os.path.basename(fn) for fn in full_dir_names]

        file_infos = []
        for fn in file_names:
            fi = {"name": os.path.basename(fn)}
            fi["size"] = os.path.getsize(fn)
            fi["modified"] = os.path.getmtime(fn)
            file_infos.append(fi)

        folder["files"] = file_infos
        folder["dirs"] = dir_names

        return folder, full_dir_names

    # ---- MISC FUNCTIONS ----

    def set_retries(self, count):
        return 0
        
    # ---- WORKSPACE ----

    def is_legal_workspace_name(self, ws_name):
        if not ws_name:
            return False

        if len(ws_name) > 255:
            return False

        if not bool(re.match('^[a-zA-Z0-9-_]+$', ws_name)):
           return False

        return True

    def does_workspace_exist(self, ws_name):
        path = self._get_workspace_path(ws_name)
        return os.path.exists(path)

    def ensure_workspace_exists(self, ws_name, flag_as__error=True):
        exists = self.does_workspace_exist(ws_name)
        if not exists:
            if flag_as__error:
                self._error(f"Workspace not found: {ws_name}")
            self.create_workspace(ws_name)

    def create_workspace(self, ws_name, description=None):
        '''
        Create the workspace directory, the __WS__ subdirectory, and the next_run file.
        '''
        path = self._get_workspace_path(ws_name)

        # MULTIPROCESS: this is the step that will fail (if any)  
        os.mkdir(path)

        # MULTIPROCESS: safe now
        # create the __WS__ subdirectory
        ws_subdir = path + "/" + utils.WORKSPACE_DIR
        os.mkdir(ws_subdir)

        # create the RUNS subdir
        runs_subdir = path + "/" + utils.RUNS_DIR
        os.mkdir(runs_subdir)

        # create the EXPERIMENTS subdir
        experiments_subdir = path + "/" + utils.EXPERIMENTS_DIR
        os.mkdir(experiments_subdir)

        # create NEXT_RUN_NAME (for extra safety, ensure file doesn't already exist)
        fn = ws_subdir + "/" + utils.WORKSPACE_NEXT
        with open(fn, "x") as tfile:
            tfile.write("1")

    def delete_workspace(self, ws_name):
        path = self._get_workspace_path(ws_name)
        #print("delete_workspace path=", path)
        shutil.rmtree(path)
        #print("AFTER, ws exists=",  os.path.exists(path))

    def get_workspace_names(self):
        names = [f.name for f in os.scandir(self.store_root_path) if f.is_dir() and f.name != utils.INFO_CONTAINER ] 
        return names

    # ---- EXPERIMENTS ----
    
    def does_experiment_exist(self, ws_name, exper_name):
        path = self._get_exper_path(ws_name, exper_name)
        return os.path.exists(path)

    def create_experiment(self, ws_name, exper_name):
        path = self._get_exper_path(ws_name, exper_name)
        os.makedirs(path)
        return True

    def append_experiment_run_name(self, ws_name, exper_name, run_name):
        path = self._get_exper_path_fn(ws_name, exper_name, utils.AGGREGATED_RUN_NAMES_FN)
        self._append_file(path, run_name + "\n")

    def get_experiment_run_names(self, ws_name, exper_name):
        path = self._get_exper_path_fn(ws_name, exper_name, utils.AGGREGATED_RUN_NAMES_FN)
        text = self._read_file(path)
        text = text[:-1]    # remove last \n char
        run_names = text.split("\n")
        return run_names

    # ---- RUN ----

    def does_run_exist(self, ws_name, run_name):
        #path = self.store_root_path + "/" + ws_name + "/" + run_name
        path = self._get_run_path(ws_name, run_name)
        return os.path.exists(path)

    def ensure_run_dir_exists(self, ws_name, run_name, flag_as__error=True):
        exists = self.does_run_exist(ws_name, run_name)

        if not exists:
            if flag_as__error:
                self._error(f"Run '{run_name}' not found in workspace '{ws_name}'")
            self._create_run_directory(ws_name, run_name)

    def get_run_log(self, ws_name, run_name):
        path = self._get_run_path(ws_name, run_name)
        fn = path + "/" + utils.RUN_LOG
        with open(fn, "r") as tfile:
            text = tfile.read()

        records = utils.load_json_records(text)
        return records

    def create_next_run_core(self, ws_name, is_parent):
        '''
        NOTE: It is normal for this function to fail - wrap it's caller with retry logic.
        '''
        # get next run number
        ws_path = self._get_workspace_path(ws_name)
        fn_next = ws_path + "/" + utils.WORKSPACE_DIR + "/" + utils.WORKSPACE_NEXT
        with open(fn_next, "r") as tfile:
            text = tfile.read()
        next_run = int(text)

        run_name = "run" + str(next_run)
        run_dir = self._get_run_path(ws_name, run_name)

        # MULTIPROCESS: here is the part that can fail if someone "got there first"
        os.mkdir(run_dir)

        # MULTIPROCESS: safe
        # update the next_run number
        with open(fn_next, "w") as tfile:
            tfile.write(str(next_run+1))

        if is_parent:
            # create NEXT_RUN_NAME (for extra safety, ensure file doesn't already exist)
            fn = run_dir + "/" + utils.WORKSPACE_NEXT
            with open(fn, "x") as tfile:
                tfile.write("1")
            
        # create the run log (for extra safety, ensure file doesn't already exist)
        fn_log = run_dir + "/" + utils.RUN_LOG
        with open(fn_log, "x") as tfile:
            pass    # just create as 0 bytes

        return run_name

    def create_next_child_core(self, ws_name, parent_name):
        '''
        NOTE: It is normal for this function to fail - wrap it's caller with retry logic.
        '''
        # get next CHILD run number
        parent_path = self._get_run_path(ws_name, parent_name)
        fn_next = parent_path + "/" + utils.WORKSPACE_NEXT
        with open(fn_next, "r") as tfile:
            text = tfile.read()
        next_run = int(text)

        run_name = parent_name + "." + str(next_run)
        run_dir = self._get_run_path(ws_name, run_name)  #       parent_path + "/" + run_name

        # MULTIPROCESS: here is the part that can fail if someone "got there first"
        os.mkdir(run_dir)

        # MULTIPROCESS: safe
        # update the next_run number
        with open(fn_next, "w") as tfile:
            tfile.write(str(next_run+1))

        # create the run log (for extra safety, ensure file doesn't already exist)
        fn_log = run_dir + "/" + utils.RUN_LOG
        with open(fn_log, "x") as tfile:
            pass    # just create as 0 bytes

        return run_name

    def get_run_names(self, ws_name):
        path = self._get_workspace_path(ws_name) + "/" + utils.RUNS_DIR
        file_objs = list(os.scandir(path))
        names = [f.name for f in file_objs if os.path.isdir(f.path) and f.name != utils.WORKSPACE_DIR]  
        #print("names=", names)
        return names

    def delete_run(self, ws_name, run_name):
        path = self._get_run_path(ws_name, run_name)
        shutil.rmtree(path)

    def copy_run(self, ws_name, run_name, ws_name2, run_name2):
        from_path = self._get_run_path(ws_name, run_name)
        to_workspace_path = self._get_workspace_path(ws_name2)
        to_path = to_workspace_path + "/" + run_name2
        if os.path.exists(to_path):
            self._error(f"Run '{run_name2}' already exists in workspace '{ws_name2}'")
        shutil.copytree(from_path, to_path)

    def copy_run_files_to_run(self, ws_name, from_run, run_wildcard, to_run, to_path):
        full_source_wildcard = self._get_run_path_fn(ws_name, from_run, run_wildcard)
        dest_folder = self._get_run_path_fn(ws_name, to_run, to_path)
        return self._copy_files(full_source_wildcard, dest_folder)


    #---- JOBS ----

    def create_info_container_if_needed(self):
        info_path = self._get_workspace_path(utils.INFO_CONTAINER)
        if not os.path.exists(info_path):
            # MULTIPROCESS: here is the first part that can fail if someone else "got there first"
            os.mkdir(info_path)

            # create the INFO DIR
            info_dir = info_path + "/" + utils.INFO_DIR
            os.mkdir(info_dir)

            # write the control file for next job number
            fn_next = info_dir + "/" + utils.JOBS_NEXT
            with open(fn_next, "w") as tfile:
                tfile.write("1")

            jobs_dir = self._get_jobs_dir()
            os.mkdir(jobs_dir)

    def create_next_job_core(self):
        '''
        NOTE: It is normal for this function to fail - wrap it's caller with retry logic.
        '''
        self.create_info_container_if_needed()

        # read next job number from control file
        info_path = self._get_workspace_path(utils.INFO_CONTAINER)
        fn_next = info_path + "/" + utils.INFO_DIR + "/" + utils.JOBS_NEXT

        with open(fn_next, "r") as tfile:
            text = tfile.read()
        next_job = int(text)

        # create the new job directory
        job_name = "job" + str(next_job) 
        job_dir = self._get_job_path(job_name)

        # MULTIPROCESS DANGER: here is the second part that can fail if someone "got there first"
        os.mkdir(job_dir)

        # MULTIPROCESS SAFE: update the next_job number
        with open(fn_next, "w") as tfile:
            tfile.write(str(next_job+1))

        # MULTIPROCESS SAFE: create the job info file
        job_dict = {}
        job_dict_text = json.dumps(job_dict)
        self.write_job_info_file(job_name, job_dict_text)

        return job_name

    def read_job_info_file(self, job_name):
        fn_job = self._get_job_file_path(job_name, utils.JOB_INFO_FN)
        return self._read_file(fn_job)

    def write_job_info_file(self, job_name, text):
        fn_job = self._get_job_file_path(job_name, utils.JOB_INFO_FN)
        self._create_file(fn_job, text)

    def get_job_names(self):
        path = self._get_jobs_dir()
        file_objs = list(os.scandir(path))
        #print("file_objs=", [obj.path for obj in file_objs])
        names = [f.name for f in file_objs if os.path.isdir(f.path) and f.name != utils.WORKSPACE_DIR]  
        return names

    def append_job_run_name(self, job_name, run_name):
        path = self._get_job_path_fn(job_name, utils.AGGREGATED_RUN_NAMES_FN)
        self._append_file(path, run_name + "\n")

    def get_job_run_names(self, job_name):
        path = self._get_job_path_fn(job_name, utils.AGGREGATED_RUN_NAMES_FN)
        text = self._read_file(path)
        text = text[:-1]    # remove last \n char
        run_names = text.split("\n")
        return run_names

    # ---- DIRECT ACCESS ----

    def list_files(self, ws, path, subdirs):
        if path:
            if not path.startswith("/"):
                path = ws + "/" + path
        else:
            path = ws

        path = self.store_root_path + "/" + path

        #print("path=", path)
        return self._list_files(path, subdirs)

    def read_store_file(self, ws, path):
        if path:
            if not path.startswith("/"):
                path = ws + "/" + path
        else:
            path = ws

        return self._read_file(path)

    # ---- FILES OBJECTS helper functions ----
    def run_files(self, ws_name, run_name, use_blobs=False):
        return RunFiles(self, ws_name, run_name, use_blobs)

    def experiment_files(self, ws_name, exper_name, use_blobs=False):
        return ExperimentFiles(self, ws_name, exper_name, use_blobs)

    def workspace_files(self, ws_name, use_blobs=False):
        return WorkspaceFiles(self, ws_name, use_blobs)

    def job_files(self, job_name, use_blobs=False):
        return JobFiles(self, job_name, use_blobs)

# ---- FILES OBJECTS ----

class FilesObject():
    def __init__(self):
        self.store = False
        self.root_path = None
        self.use_blobs = False

    def create_file(self, path, text):
        store_fn = self.root_path + "/" + path
        self.store._create_file(store_fn, text)

    def append_file(self, fn, text):
        store_fn = self.root_path + "/" + fn
        self.store._append_file(store_fn, text)

    def read_file(self, fn):
        store_fn = self.root_path + "/" + fn
        return self.store._read_file(store_fn)

    def upload_file(self, fn, source_fn):
        store_fn = self.root_path + "/" + fn
        self.store._copy_file(source_fn, store_fn) 

    def upload_files(self, folder, source_wildcard, exclude_dirs_and_files=[]):
        store_folder = self.root_path + "/" + folder
        return self.store._copy_files(source_wildcard, store_folder, exclude_dirs_and_files=exclude_dirs_and_files)

    def download_file(self, fn, dest_fn):
        store_fn = self.root_path + "/" + fn
        self.store._copy_file(store_fn, dest_fn) 

    def download_files(self, wildcard, dest_folder):
        store_wildcard = self.root_path + "/" + wildcard
        return self.store._copy_files(store_wildcard, dest_folder)

    def get_filenames(self, wildcard="*", full_paths=False):
        store_wildcard = self.root_path + "/" + wildcard
        return self.store._get_filesnames(store_wildcard, relative_paths=not full_paths)
        
    def delete_files(self, wildcard):
        wild_path = self.root_path + "/" + wildcard
        return self.store._delete_files(wild_path)

    def does_file_exist(self, fn):
        fn_full = self.root_path + "/" + fn
        #print("does_file_exist: fn_full=", fn_full)
        return os.path.exists(fn_full)

class RunFiles(FilesObject):
    def __init__(self, store, ws_name, run_name, use_blobs=False):
        self.store = store
        self.root_path = self.store._get_run_path(ws_name, run_name)
        self.use_blobs = use_blobs

class WorkspaceFiles(FilesObject):
    def __init__(self, store, ws_name, use_blobs=False):
        self.store = store
        self.root_path = self.store._get_workspace_path(ws_name)
        self.use_blobs = use_blobs

class ExperimentFiles(FilesObject):
    def __init__(self, store, ws_name, exper_name, use_blobs=False):
        self.store = store
        self.root_path = self.store._get_exper_path(ws_name, exper_name)
        self.use_blobs = use_blobs

class JobFiles(FilesObject):
    def __init__(self, store, job_name, use_blobs=False):
        self.store = store
        self.root_path = self.store._get_job_path(job_name)
        self.use_blobs = use_blobs
