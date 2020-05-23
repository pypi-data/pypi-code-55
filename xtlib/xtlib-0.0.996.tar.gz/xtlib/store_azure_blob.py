# store_azure_blob.py: implements Azure-based store support using containers and blobs

from azure.storage.blob import AppendBlobService, BlockBlobService, PublicAccess
from contextlib import redirect_stderr
#import azure.storage.common.retry as retry
import re
import os
import uuid
import sys
import time
import json
import shutil
import numpy as np
from fnmatch import fnmatch

from . import utils
from . import store_azure_file

class StoreAzureBlob():
    '''
    Implements STORE blob access for Azure storage.  Note, we use "redirect_stderr" to 
    suppress the STDERR output from Azures API's when they have an _error to keep our
    console output a bit cleaner (easier to follow what's happening).
    '''
    def __init__(self, storage_id, storage_key, sas_token=None, max_retries=10, suppress_azure_stderr=False):
        self.blob_client = None
        self.storage_id = storage_id
        self.storage_key = storage_key

        #print("creating BlockBlobService with account_name=", storage_id)
        self.bs = BlockBlobService(account_name=storage_id, account_key=storage_key) 
        self.append_bs = AppendBlobService(account_name=storage_id, account_key=storage_key) 

        self.max_retries = None
        self.set_retries(max_retries)

        #self.bs.retry_callback = retry_callback
        # self.bs.request_callback = request_callback
        # self.bs.response_callback = response_callback

    # ---- INTERNAL HELPERS ----
    def _error(self, msg):
        raise Exception(f"error - {msg}")

    def _check_ws_name(self, ws_name):
        if not self.is_legal_workspace_name(ws_name):
           raise Exception("error: Illegal Azure workspace name (must be >= 3 alphanumeric chars, dashes OK, no space or underscore chars)")

    def _get_job_dir(self, job_name):
        return utils.JOBS_DIR + "/" + job_name 

    def _get_job_path_fn(self, job_name, blob_path):
        return utils.JOBS_DIR + "/" + job_name + "/" + blob_path

    def _make_workspace_path_fn(self, ws, fn):
        # note: path does not include the "ws"
        return utils.WORKSPACE_DIR + "/" + fn

    def _exper_path(self, exper_name):
        return utils.EXPERIMENTS_DIR + "/" + exper_name 

    def _exper_path_fn(self, exper_name, fn):
        return utils.EXPERIMENTS_DIR + "/" + exper_name + "/" + fn

    def _run_path(self, run_name):
        return utils.RUNS_DIR + "/" + run_name 

    def _make_run_path_fn(self, run_name, fn):
        return utils.RUNS_DIR + "/" + run_name + "/" + fn

    def _remove_first_node(self, path):
        ''' remove first node of path '''
        new_path = "/".join(path.split("/")[1:])
        return new_path

    def _create_blob(self, ws_name, blob_path, text, fail_if_exists=False):
        if fail_if_exists:
            # error if blob already exists 
            #print("_create_blob: blob_path=", blob_path)
            self.bs.create_blob_from_text(ws_name, blob_path, text, if_none_match="*")
        else:
            # no error if blob already exists (just overwrite it)
            self.bs.create_blob_from_text(ws_name, blob_path, text)

    def _append_blob(self, ws_name, blob_path, text):
        # create blob if it doesn't exist
        if not self.append_bs.exists(ws_name, blob_path):
            self.append_bs.create_blob(ws_name, blob_path)

        #print("append: ws_name=", ws_name, ", blob_path=", blob_path, ", text=", text)
        self.append_bs.append_blob_from_text(ws_name, blob_path, text)

    def _append_blob_with_rewrite(self, container, blob_path, text):
        ''' 
        Appends text to a normal blob blob by reading and then rewriting the entire blob.
        Correctly handles concurrency/race conditions.
        Recommended for lots of small items (like 10,000 run names).

        Note: we turn off retries on azure CALL-level so that we can retry on 
        OUR CALL-level.
        '''
        # experimental local retry loop
        old_retry = self.bs.retry
        self.bs.retry = utils.make_retry_func(0)
        succeeded = False

        for i in range(20):
            
            try:
                if self.bs.exists(container, blob_path):
                    # read prev contents
                    blob = self.bs.get_blob_to_text(container, blob_path)
                    # append our text
                    new_text = blob.content + text
                    # write blob, ensuring etag matches (no one updated since above read)
                    self.bs.create_blob_from_text(container, blob_path, new_text, if_match=blob.properties.etag)
                else:
                    # if no previous blob, just try to create it
                    self.bs.create_blob_from_text(container, blob_path, text)
            except BaseException as ex:
                sleep_time = np.random.random()*4
                print("XT store received an expected azure exception; will backoff for {:.4f} secs [retry #{}]".format(sleep_time, i+1))
                time.sleep(sleep_time)
            else:
                succeeded = True
                break

        # restore retry
        self.bs.retry = old_retry

        if not succeeded:
            raise Exception("_append_blob_with_rewrite failed (too many retries)")

    def _read_blob(self, ws_name, blob_path):
        blob = self.bs.get_blob_to_text(ws_name, blob_path)
        return blob.content

    def _list_wild_blobs(self, ws_name, ws_wildcard):
        #print("_list_wild_blobs: ws_name=", ws_name, ", ws_wildcard=", ws_wildcard)
        wild_base = os.path.basename(ws_wildcard)

        if not "*" in wild_base and not "." in wild_base:
            # handle case where wild_base has no wildcards
            names = [blob.name for blob in self.bs.list_blobs(ws_name, prefix=ws_wildcard)]
        else:
            # handle case with wildcards
            wild_dir = os.path.dirname(ws_wildcard)
            names = [blob.name for blob in self.bs.list_blobs(ws_name, prefix=wild_dir)]
            #print("before fnmatch, names=", names)

            names = [name for name in names if fnmatch(name, ws_wildcard)]
        return names

    def _delete_blobs(self, ws_name, ws_wildcard):
        delete_count = 0

        for bn in self._list_wild_blobs(ws_name, ws_wildcard):
            self.bs.delete_blob(ws_name, bn)
            delete_count += 1

        return delete_count

    def _wildcard_match_in_list(self, source, name_list):
        matches = []

        if name_list:
            matches = [name for name in name_list if fnmatch(source, name)]
            
        return len(matches) > 0

    def _upload_files(self, ws_name, ws_path, source_wildcard, recursive=False, exclude_dirs_and_files=[]):
        copied_files = []
        #print("_upload_files: source_wildcard=", source_wildcard)

        # handle special "**" for recursive copy
        if source_wildcard == "**":
            recursive = True
            source_wildcard = "*"

        utils.diag("exclude_dirs_and_files={}".format(exclude_dirs_and_files))
        
        for source_fn in utils.glob(source_wildcard):
            #print("source_fn=", source_fn)
            source_name = os.path.basename(source_fn)
            if self._wildcard_match_in_list(source_name, exclude_dirs_and_files):
                # omit processing this file or directory
                utils.diag("skipping upload of file/dir: {}".format(source_name))
                continue

            if os.path.isfile(source_fn):
                utils.diag("uploading FILE: " + source_fn)
                blob_path = ws_path + "/" + source_name
                #print("ws_name=", ws_name, ", blob_path=", blob_path, ", source_fn=", source_fn)
                result = self.bs.create_blob_from_path(ws_name, blob_path, source_fn)
                #print("after bs.create_blob_from_path, result=", result)
                copied_files.append(source_fn)
            elif os.path.isdir(source_fn) and recursive:
                # copy subdir
                utils.diag("uploading DIR: " + source_fn)
                copied  = self._upload_files(ws_name, ws_path + "/" + source_name, source_fn + "/*", recursive=recursive, 
                    exclude_dirs_and_files=exclude_dirs_and_files)
                copied_files = copied_files + copied

        return copied_files

    def _get_blob_dir(self, path):
        index = path.rfind("/")
        index2 = path.rfind("\\")
        index = max(index, index2)

        if index > -1:
            path = path[index+1:]
        return path

    def _download_files(self, ws_name, ws_wildcard, dest_folder):
        files_copied = []

        names = self._list_wild_blobs(ws_name, ws_wildcard)
        #print("names=", names)
        blob_dir = os.path.dirname(ws_wildcard)
        bd_index = 1 + len(blob_dir)   # add for for trailing slash
        #print("blob_dir=", blob_dir, ", bd_index=", bd_index)

        for bn in names:
            base_bn = bn[bd_index:]
            dest_fn = dest_folder + "/" + base_bn

            utils.ensure_dir_exists(file=dest_fn)
            self.bs.get_blob_to_path(ws_name, bn, dest_fn)
            files_copied.append(dest_fn)    

        return files_copied

    def _copy_files(self, ws_name, ws_wildcard, to_path):
        ''' copy files from one blob folder to another, within the same workspace/container.
        example call:  _copy_files("ws1", "runs/run8/before*", "runs/run13/before")
        ''' 
        files_copied = []

        #print("_copy_files: ws_name=", ws_name, ", ws_wildcard=", ws_wildcard, ", to_path=", to_path)
        names = self._list_wild_blobs(ws_name, ws_wildcard)
        #print("names=", names)
        blob_dir = os.path.dirname(ws_wildcard)
        bd_index = 1 + len(blob_dir)   # add for for trailing slash
        #print("blob_dir=", blob_dir, ", bd_index=", bd_index)

        for bn in names:
            base_bn = bn[bd_index:]
            #print("blob_dir=", blob_dir, ", bd_index=", bd_index, ", base_bn=", base_bn)
            dest_path = to_path + "/" + base_bn

            # COPY BLOB
            source_blob_url = self.bs.make_blob_url(ws_name, bn)
            #print("blob.name=", source_blob.name, ", url=", source_blob_url, ", dest_blob_path=", dest_blob_path)
            self.bs.copy_blob(ws_name, dest_path, source_blob_url)

            files_copied.append(base_bn)

        return files_copied

    def _list_files(self, wild_path, subdirs=0):

        root = self.storage_id
        dd = {"store_name": "XT Azure Store ({})".format(root)}

        if wild_path == "/":
            folder, folder_names = self._get_root_folders()
            folders = [ folder ]

            if subdirs:
                base_path = ""
                for ws_name in folder_names:

                    # get blobs from AZURE
                    #print("reading blobs for ws=", ws_name)
                    blobs  = self.bs.list_blobs(ws_name, prefix=base_path)
                     
                    ws_folders = self._build_folders_from_blobs(blobs, ws_name, 
                        base_path, subdirs)

                    folders += ws_folders
        else:
            # split wild_path into workspace and rest
            ws_name, base_path = self._get_first_dir(wild_path)

            # get blobs from AZURE
            blobs  = self.bs.list_blobs(ws_name, prefix=base_path)

            folders = self._build_folders_from_blobs(blobs, ws_name, base_path, subdirs)
        
        # filter folders as per subdirs
        if not subdirs is True:
            # subdirs is set to an int value
            #print("filtering by subdirs=", subdirs)
            folders = [f for f in folders if f["level"] <= subdirs]
 
        dd["folders"] = folders
        return dd

    def _get_first_dir(self, path):
        first_dir = None
        rest = None

        if path:
            if path.startswith("/"):
                path = path[1:]
            if "/" in path:
                index = path.index("/")
                first_dir = path[0:index]
                rest = path[index+1:]
                #print("path=", path, ", first_dir=", first_dir)
            else:
                first_dir = path
                if first_dir.endswith("/*"):
                    first_dir = first_dir[0:-2]
                rest = ""

        return first_dir, rest

    def _build_folders_from_blobs(self, blobs, ws_name, base_path, subdirs):
        folders_by_name = {}
        folders = []    # ordered list of folders

        base_len = len(base_path)
        if base_path.endswith("*"):
            base_len -= 1
        if base_path:
            base_len += 1    # for trailing slash
            
        base_folder = self._get_folder(folders, folders_by_name, ws_name, base_path, base_len)
        #print("base_folder=", base_folder)

        for i, blob in enumerate(blobs):

            full_blob_path = blob.name
            #print("full_blob_path=", full_blob_path)

            file_path = os.path.dirname(full_blob_path)
            parent_path = os.path.dirname(file_path)

            if subdirs or file_path == base_path:
                # add file to its folder
                folder = self._get_folder(folders, folders_by_name, ws_name, file_path, base_len)
                
                # create a new file entry
                fi = {"name": os.path.basename(blob.name)}
                fi["size"] = blob.properties.content_length 
                fi["modified"] = blob.properties.last_modified.timestamp()
                folder["files"].append(fi)

            if subdirs:
                # add all path parts to their parent folders
                child_path = file_path

                while len(parent_path) >= len(base_path):    # and parent_path != "/":
                    #print("  parent_path=", parent_path, ", child_path=", child_path, ", base_path=", base_path)
                    if parent_path:
                        parent_folder = self._get_folder(folders, folders_by_name, ws_name, parent_path, base_len)
                    else:
                        parent_folder = base_folder

                    # add child dir, if needed
                    child_name = os.path.basename(child_path)
                    dirs = parent_folder["dirs"]
                    if not child_name in dirs:
                        dirs.append(child_name)

                    # stop when base_path folder has been added to
                    if parent_path == base_path:
                        break

                    # process next level up
                    child_path = parent_path
                    parent_path = os.path.dirname(parent_path)
            else:
                # just process the left-most directory part of rel_path
                rel_file_path = file_path[base_len:]
                left_most_path, rest = self._get_first_dir(rel_file_path)
                #print("FIRST left_most_path=", left_most_path, ", rest=", rest)
                if left_most_path:
                    # add child dir, if needed
                    dirs = base_folder["dirs"]
                    child_name = os.path.basename(left_most_path)
                    if not child_name in dirs:
                        dirs.append(child_name)
        
        return folders

    def _get_folder(self, folders, folders_by_name, ws_name, path, base_name_len):
        if not path in folders_by_name:
            # create a new folder
            display_name = "/" + ws_name 
            if path and path != "/":
                display_name += "/" + path
            rel_path = path[base_name_len:]
            #print("rel_path=", rel_path)

            folder = {"folder_name": display_name}
            folder["dirs"] = []
            folder["files"] = []
            folder["level"] = 1 + rel_path.count("/") if rel_path else 0
            folders_by_name[path] = folder
            folders.append(folder)

            #print("folder added: name=", display_name, ", level=", folder["level"])
        
        folder = folders_by_name[path]
        return folder

    def _get_root_folders(self):
        folder_names = self.get_workspace_names()
        folder_names.append("xt-store-info")

        folder = {"folder_name": "/"}
        folder["level"] = 0
        folder["files"] = []
        folder["dirs"] = folder_names

        return folder, folder_names

    # ---- MISC FUNCTIONS ----

    def set_retries(self, count):

        old_count = self.max_retries
        self.max_retries = count

        # bug workaround: standard Retry classes don't retry status=409 (container is being deleted)
        #import azure.storage.common.retry as retry
        #self.bs.retry = retry.LinearRetry(backoff=5, max_attempts=count).retry
        #self.append_bs.retry = retry.LinearRetry(backoff=5, max_attempts=count).retry

        self.bs.retry = utils.make_retry_func(count)
        self.append_bs.retry = utils.make_retry_func(count)

        return old_count
        
    # ---- WORKSPACES ----

    def is_legal_workspace_name(self, ws_name):

        if not bool(re.match('^[a-zA-Z0-9-]+$', ws_name)):
           return False
        
        if len(ws_name) < 3:
           return False

        return True

    def does_workspace_exist(self, ws_name):
        #print("does_workspace_exist: ws_name=", ws_name)
        self._check_ws_name(ws_name)
        return self.bs.exists(container_name=ws_name)

    def ensure_workspace_exists(self, ws_name, flag_as__error=True):
        self._check_ws_name(ws_name)
        exists = self.does_workspace_exist(ws_name)
        if not exists:
            if flag_as__error:
                self._error(f"Workspace not found: {ws_name}")
            self.create_workspace(ws_name)

    def create_workspace(self, ws_name, description=None):
        ''' create workspace as top level container '''
        self._check_ws_name(ws_name)

        # note: this operation often must retry several times if same container has just been deleted
        #print("creating workspace=", ws_name)

        # MULTIPROCESS: this is the step that will fail (if any)  
        result = self.bs.create_container(ws_name)
        if not result:
            self._error("could not create workspace: " + ws_name)

        # MULTIPROCESS: safe now

        # create a holder file for RUNS directory
        runs_holder_fn = utils.RUNS_DIR + "/" + utils.HOLDER_FILE
        self._create_blob(ws_name, runs_holder_fn, "1", True)

        # create a holder file for EXPERIMENTS directory
        experiments_holder_fn = utils.EXPERIMENTS_DIR + "/" + utils.HOLDER_FILE
        self._create_blob(ws_name, experiments_holder_fn, "1", True)

        # create NEXT_RUN_NAME (for extra safety, ensure file doesn't already exist)
        blob_fn = utils.WORKSPACE_DIR + "/" + utils.WORKSPACE_NEXT
        self._create_blob(ws_name, blob_fn, "1", True)


    def delete_workspace(self, ws_name):
        result = self.bs.delete_container(ws_name)    

        if not result:
            self._error("could not delete workspace: " + ws_name)

        return result

    def get_workspace_names(self):
        containers = self.bs.list_containers()

        names = [c.name for c in containers if self.workspace_files(c.name, use_blobs=True).does_file_exist(utils.WORKSPACE_LOG)]
        return names

    # ---- EXPERIMENTS ----
    
    def does_experiment_exist(self, ws_name, exper_name):
        path = self._exper_path_fn(exper_name, utils.HOLDER_FILE)
        return self.bs.exists(ws_name, path)

    def create_experiment(self, ws_name, exper_name):
        path = self._exper_path_fn(exper_name, utils.HOLDER_FILE)
        #print("create_experiment: path=", path)
        return self._create_blob(ws_name, path, "1")

    def append_experiment_run_name(self, ws_name, exper_name, run_name):
        path = self._exper_path_fn(exper_name, utils.AGGREGATED_RUN_NAMES_FN)
        self._append_blob_with_rewrite(ws_name, path, run_name + "\n")

    def get_experiment_run_names(self, ws_name, exper_name):
        path = self._exper_path_fn(exper_name, utils.AGGREGATED_RUN_NAMES_FN)
        if self.bs.exists(ws_name, path):
            text = self._read_blob(ws_name, path)
            text = text[:-1]    # remove last \n char
            run_names = text.split("\n")
        else:
            run_names = []
        return run_names

    # ---- RUNS ----

    def does_run_exist(self, ws_name, run_name):
        # we cannot ensure the run directory exists since it's a virtual directory for blob
        # so we test for the run log file
        blob_path = self._run_path(run_name) + "/run.log"
        #print("ws_name=", ws_name, ", blob_path=", blob_path)
        return self.bs.exists(container_name=ws_name, blob_name=blob_path)

    # def ensure_run_exists(self, ws_name, run_name, flag_as__error=True):
    #     exists = self.does_run_exist(ws_name, run_name)
    #     if not exists:
    #         if flag_as__error:
    #             self._error(f"Run '{run_name}' not found in workspace '{ws_name}'")
    #         self._create_run_directory(ws_name, run_name)

    def get_run_names(self, ws_name):
        # enumerate all blobs in workspace (ouch)
        names = [b.name[0:-1] for b in self.bs.list_blobs(ws_name, prefix=utils.RUNS_DIR + "/run", delimiter="/")]

        # remove returned prefix on names
        plen = len(utils.RUNS_DIR + "/")
        names = [name[plen:] for name in names]

        #print("get_run_names: names=", names)
        return names

    def delete_run(self, ws_name, run_name):
        # run dir is a virtual directory that cannot be directly deleted
        # so, we need to enumerate and delete each one
        
        # since we are deleting from the list we are enumerating, safest to grab the whole list up frong
        blobs = list(self.bs.list_blobs(ws_name, self._run_path(run_name) + "/"))
        for blob in blobs:
            self.bs.delete_blob(ws_name, blob.name)   

    def copy_run(self, source_workspace_name, source_run_name, dest_workspace_name, dest_run_name):
        if self.does_run_exist(dest_workspace_name, dest_run_name):
            self._error(f"destination run already exists: ws={dest_workspace_name}, run={dest_run_name}")

        # copy a single blob at a time
        #for source_blob_path in self.bs.list_blob_names(source_workspace_name, source_run_name):
        for source_blob in self.bs.list_blobs(source_workspace_name, self._run_path(source_run_name)  + "/"):
            source_blob_url = self.bs.make_blob_url(source_workspace_name, source_blob.name)
            dest_blob_path = self._run_path(dest_run_name)  + "/" + self._remove_first_node(source_blob.name)
            #print("blob.name=", source_blob.name, ", url=", source_blob_url, ", dest_blob_path=", dest_blob_path)
            self.bs.copy_blob(dest_workspace_name, dest_blob_path, source_blob_url)

    def get_run_log(self, ws_name, run_name):
        blob_path = self._run_path(run_name) + "/" + utils.RUN_LOG
        
        if not self.bs.exists(ws_name, blob_path):
            # limited support for old-style run logging 
            blob_path = run_name + "/" + utils.RUN_LOG

        #print("blob_path=", blob_path)
        if not self.bs.exists(ws_name, blob_path):
            utils.user_error("unknown run: ws={}, run_name={}".format(ws_name, run_name))

        #print("get_run_log: ws_name=", ws_name, ", blob_path=", blob_path)

        # watch out for 0-length blobs (azure will throw retryable exception if you use "get_blob_to_text")
        blob = self.bs.get_blob_properties(ws_name, blob_path)
        #print("blob.properties.content_length=", blob.properties.content_length)
        lines = []

        if blob.properties.content_length:
            blob = self.bs.get_blob_to_text(ws_name, blob_path)
            text = blob.content
            #print("get_run_log: text=", text)

            lines = text.split("\n")
            #print("lines=", lines)
            lines = [json.loads(line) for line in lines if line.strip()]

        return lines

    # def create_run_directory(self, ws_name, run_name):
    #     pass   # nothing to do for blobs here

    def create_next_run_core(self, ws_name, is_parent):
        '''
        NOTE: It is normal for this function to fail - wrap it's caller with retry logic.
        '''
        #print("create_next_run_core: ws_name=", ws_name)
        self._check_ws_name(ws_name)    

        # get next run number
        fn_next = utils.WORKSPACE_DIR + "/" + utils.WORKSPACE_NEXT
        #print("reading next num, fn_next=", fn_next)

        text = self._read_blob(ws_name, fn_next)
        next_run = int(text)
        flag_created = False
        #print("next_run=", next_run)

        # experimental local retry loop
        for i in range(10):
            run_name = "run" + str(next_run)
            run_dir = self._run_path(run_name) 

            # due to Azure restriction, we cannot create run_dir explictly

            # MULTIPROCESS: here is the part that can fail if someone "got there first"
            # we create a FLAG blob (contents="1"), whose successful creation indicates we "got here first"
            fn_flag = run_dir + "/" + utils.HOLDER_FILE

            try:
                if i:
                    print("trying to create flag file: ", fn_flag)
                self._create_blob(ws_name, fn_flag, "1", True)   
                flag_created = True 
                break
            except:
                time.sleep(.5)

            # try next available run number
            next_run += 1
            #print("created flag file=", fn_flag)

        if not flag_created:
            raise Exception("create_next_run_core timed out trying to find next run directory")

        # TODO: there is a timing issue that rfernand has experienced on 6/3/2019 - if xt gets control-c interuped 
        # at this location, we have created the run dir without updating the fn_next, which will cause
        # next run creator to fail (after multiple retires trying to create the run dir).
        # ----
        # hit this again on 6/21/2019.  Need to fix this - otherwise, they workspace is TOAST when it happens!
        #----
        # above "try/except/increment next_run" seems to work in the simplest case, but should rework this to use
        # the Azure serial number approach to know when retry is needed, without invoking Azure exceptions.

        # MULTIPROCESS: safe
        # update the next_run number
        text = str(next_run+1)
        self._create_blob(ws_name, fn_next, text)
        #print("updated next_run: fn=", fn_next)

        if is_parent:
            # create NEXT_RUN_NAME (for extra safety, ensure file doesn't already exist)
            blob_fn = run_dir + "/" + utils.WORKSPACE_NEXT
            self._create_blob(ws_name, blob_fn, "1", True)

        return run_name

    def create_next_child_core(self, ws_name, parent_name):
        '''
        NOTE: It is normal for this function to fail - wrap it's caller with retry logic.
        '''
        #print("create_next_run_core: ws_name=", ws_name)
        self._check_ws_name(ws_name)    

        # get next run number
        fn_next = self._run_path(parent_name)  + "/" + utils.WORKSPACE_NEXT
        #print("reading next num, fn_next=", fn_next)

        text = self._read_blob(ws_name, fn_next)
        next_run = int(text)
        #print("next_run=", next_run)

        run_name = parent_name + "." + str(next_run)
        run_dir = self._run_path(run_name) 

        # due to Azure restriction, we cannot create run_dir explictly

        # MULTIPROCESS: here is the part that can fail if someone "got there first"
        # we create a FLAG blob (contents="1"), whose successful creation indicates we "got here first"
        fn_flag = run_dir + "/" + utils.HOLDER_FILE
        self._create_blob(ws_name, fn_flag, "1", True)    
        #print("created flag file=", fn_flag)

        # MULTIPROCESS: safe
        # update the next_run number
        text = str(next_run+1)
        self._create_blob(ws_name, fn_next, text)
        #print("updated next_run: fn=", fn_next)

        return run_name

    def copy_run_files_to_run(self, ws_name, from_run, run_wildcard, to_run, to_path):
        from_path = self._make_run_path_fn(from_run, run_wildcard)
        dest_path = self._make_run_path_fn(to_run, to_path)
        return self._copy_files(ws_name, from_path, dest_path)

    #---- JOBS ----

    def create_info_container_if_needed(self):
        info_container = utils.INFO_CONTAINER
        if not self.does_workspace_exist(info_container):

            # MULTIPROCESS DANGER: here is the first part that can fail if someone else "got there first"
            if self.bs.create_container(info_container):
        
                # write the control file for next job number
                info_dir = utils.INFO_DIR
                fn_next = info_dir + "/" + utils.JOBS_NEXT

                # creating fn_next will auto-create info_dir 
                self._create_blob(info_container, fn_next, "1")

                # create the JOBS dir
                jobs_dir_holder_fn = utils.JOBS_DIR + "/" + utils.HOLDER_FILE
                self._create_blob(info_container, jobs_dir_holder_fn, "1")

    def create_next_job_core(self):
        '''
        NOTE: It is normal for this function to fail - wrap it's caller with retry logic.
        '''
        self.create_info_container_if_needed()

        # read next job number from control file
        info_container = utils.INFO_CONTAINER
        info_dir = utils.INFO_DIR
        fn_next = info_dir + "/" + utils.JOBS_NEXT

        text = self._read_blob(info_container, fn_next)
        next_job = int(text)

        # create the new job directory / job info file
        job_name = "job" + str(next_job) 
        fn_job = self._get_job_path_fn(job_name, utils.JOB_INFO_FN)

        # MULTIPROCESS DANGER: here is the second part that can fail if someone "got there first"
        self._create_blob(info_container, fn_job, "{}")

        # MULTIPROCESS: safe
        # update the next_job number
        self._create_blob(info_container, fn_next, str(next_job+1))

        return job_name

    def read_job_info_file(self, job_name):
        fn_job = self._get_job_path_fn(job_name, utils.JOB_INFO_FN)
        return self._read_blob(utils.INFO_CONTAINER, fn_job)

    def write_job_info_file(self, job_name, text):
        fn_job = self._get_job_path_fn(job_name, utils.JOB_INFO_FN)
        self._create_blob(utils.INFO_CONTAINER, fn_job, text)

    def create_job_dir(self, job_name):
        self.create_info_container_if_needed()
        job_dir_path = self._get_job_path_fn(job_name, utils.HOLDER_FILE)

        # MULTIPROCESS: safe, because only 1 user will try to create the job dir (?)
        if not self.bs.exists(utils.INFO_CONTAINER, job_dir_path):
            self._create_blob(utils.INFO_CONTAINER, job_dir_path, "1")

    def get_job_names(self):
        path = utils.JOBS_DIR 
        names = [ b.name[5:-1] for b in self.bs.list_blobs(utils.INFO_CONTAINER, prefix=utils.JOBS_DIR + "/job", delimiter="/") ]
        #print("names=", names)
         
        # sort by increasing job number
        names.sort(key=lambda name: int(name[3:]))
        return names

    def append_job_run_name(self, job_name, run_name):
        path = self._get_job_path_fn(job_name, utils.AGGREGATED_RUN_NAMES_FN)
        self._append_blob_with_rewrite(utils.INFO_CONTAINER, path, run_name + "\n")

    def get_job_run_names(self, job_name):
        #print("getting job run_names for", job_name)
        path = self._get_job_path_fn(job_name, utils.AGGREGATED_RUN_NAMES_FN)
        if self.bs.exists(utils.INFO_CONTAINER, path):
            text = self._read_blob(utils.INFO_CONTAINER, path)
            text = text[:-1]    # remove last \n char
            run_names = text.split("\n")
        else:
            run_names = []
        return run_names

    # ---- DIRECT ACCESS ----

    def list_files(self, ws, path, subdirs=0):
        if path == ".":
            path = ""

        if path:
            if not path.startswith("/"):
                path = ws + "/" + path
        else:
            path = ws

        #print("path=", path)
        return self._list_files(path, subdirs)

    def read_store_file(self, ws, path):
        if path:
            if not path.startswith("/"):
                path = ws + "/" + path
        else:
            path = ws

        # split wild_path into workspace and rest
        ws_name, base_path = self._get_first_dir(path)
        return self._read_blob(ws_name, base_path)

    # ---- FILES OBJECTS helper functions ----

    def run_files(self, ws_name, run_name, use_blobs=False):
        if use_blobs:
            return RunBlobs(self, ws_name, run_name)
        else:
            return store_azure_file.RunFiles(self, ws_name, run_name)

    def experiment_files(self, ws_name, exper_name, use_blobs=False):
        if use_blobs:
            return ExperimentBlobs(self, ws_name, exper_name)
        else:
            return store_azure_file.ExperimentFiles(self, ws_name, exper_name)

    def workspace_files(self, ws_name, use_blobs=False):
        if use_blobs:
            return WorkspaceBlobs(self, ws_name)
        else:
            return store_azure_file.WorkspaceFiles(self, ws_name)

    def job_files(self, job_name, use_blobs=False):
        if use_blobs:
            return JobBlobs(self, job_name)
        else:
            return store_azure_file.JobFiles(self, job_name)

# ---- FILES OBJECTS ----

class BlobsObject():
    def __init__(self):
        self.store = False
        self.container = None
        self.base_path = False

    # need for FilesObject
    # def get_dir_fn(self, path):
    #     full_path = self.root_path + path
    #     dir_path = os.path.dirname(full_path)
    #     fn = os.path.basename(full_name)
    #     return dir, fn

    def _expand_path(self, path):
        if self.base_path:
            path = self.base_path + "/" + path
        return path

    def create_file(self, path, text, block_size=None):
        path = self._expand_path(path)
        return self.store._create_blob(self.container, path, text)

    def append_file(self, fn, text):
        path = self._expand_path(fn)
        return self.store._append_blob(self.container, path, text)

    def read_file(self, fn):
        path = self._expand_path(fn)
        return self.store._read_blob(self.container, path)

    def upload_file(self, fn, source_fn):
        path = self._expand_path(fn)
        return self.store.bs.create_blob_from_path(self.container, path, source_fn)

    def upload_files(self, folder, source_wildcard, recursive=False, exclude_dirs_and_files=[]):
        path = self._expand_path(folder)
        return self.store._upload_files(self.container, path, source_wildcard, recursive=recursive, 
            exclude_dirs_and_files=exclude_dirs_and_files)

    def download_file(self, fn, dest_fn):
        path = self._expand_path(fn)
        utils.ensure_dir_exists(file=dest_fn)
        #print("self.container=", self.container, ", path=", path)
        return self.store.bs.get_blob_to_path(self.container, path, dest_fn)

    def download_files(self, wildcard, dest_folder):
        path = self._expand_path(wildcard)
        return self.store._download_files(self.container, path, dest_folder)

    def get_filenames(self, wildcard="*", full_paths=False):
        path = self._expand_path(wildcard)
        names = self.store._list_wild_blobs(self.container, path)

        if not full_paths:
            # convert to relative paths (relative to the path for this job/run/experiment/workspace)
            path_len = len(path) - len(wildcard)
            #print("PRE names=", names)
            names = [ name[path_len:] for name in names ]
            #print("POST names=", names)
        return names

    def delete_files(self, wildcard):
        path = self._expand_path(wildcard)
        return self.store._delete_blobs(self.container, path)

    def does_file_exist(self, fn):
        path = self._expand_path(fn)
        #print("does_file_exist: fn=", fn, ", path=", path)
        return self.store.bs.exists(self.container, path)

class WorkspaceBlobs(BlobsObject):
    def __init__(self, store, ws_name):
        self.store = store
        self.container = ws_name
        self.base_path = utils.WORKSPACE_DIR

class RunBlobs(BlobsObject):
    def __init__(self, store, ws_name, run_name):
        self.store = store
        self.container = ws_name
        self.base_path = utils.RUNS_DIR + "/" + run_name

class ExperimentBlobs(BlobsObject):
    def __init__(self, store, ws_name, exper_name):
        self.store = store
        self.container = ws_name
        self.base_path = utils.EXPERIMENTS_DIR + "/" + exper_name

class JobBlobs(BlobsObject):
    def __init__(self, store, job_name):
        self.store = store
        self.container = utils.INFO_CONTAINER
        self.base_path = utils.JOBS_DIR + "/" + job_name
