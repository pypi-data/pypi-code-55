# store_azure_file.py: implements XT Store File API using Azure-based file system

from azure.storage.file.fileservice import FileService
from contextlib import redirect_stderr
#import azure.storage.common.retry as retry
import re
import os
import uuid
import sys
import time
import json
from fnmatch import fnmatch

from . import utils

# ---- FILES OBJECTS ----

class FilesObject():
    def __init__(self, store_azure_blob, container, base_path):
        self.base_path = container + "/" + base_path
        self.share_name = "xt-fileshare"
        self.block_size = 1024

        # create the file service
        storage_id = store_azure_blob.storage_id
        storage_key = store_azure_blob.storage_key
        self.fs = FileService(account_name=storage_id, account_key=storage_key)

        # create share, if needed
        if not self.fs.exists(self.share_name):
            self.fs.create_share(self.share_name)

    def _create_dir(self, dir_name):
        ''' create directory by creating each node '''
        # ensure all node separators are "/"
        dir_name = dir_name.replace("\\", "/")

        parts = dir_name.split("/")
        path = ""
        for part in parts:
            path = path + "/" + part if path else part
            # assumption: its faster to just try and fail, rather that ask exist and then call create when needed
            #print("creating dir=", path)
            self.fs.create_directory(self.share_name, path)

    def _get_dir_fn(self, path, is_write=False):
        full_path = self.base_path + "/" + path if path else self.base_path

        # split full_path into dir and fn (as required by file service)
        dir_name = os.path.dirname(full_path)
        fn = os.path.basename(full_path)

        # if this is a write operation, create the directory if needed
        #print("is_write=", is_write, ", dir_name=", dir_name, ", fn=", fn)
        if is_write and not self.fs.exists(self.share_name, dir_name):
            #print("dir doesn't yet exist - creating dir=", dir_name)
            self._create_dir(dir_name)

        return dir_name, fn

    def create_file(self, path, text, block_size=None):
        if not block_size:
            block_size = self.block_size

        dir_name, fn = self._get_dir_fn(path, is_write=True)
        self.fs.create_file(self.share_name, dir_name, fn, content_length=0, metadata={"append_length": "0", "block_size": str(block_size)})   
        print("file created")

        return self.append_file(path, text)

    def append_file(self, fn, text):
        dir_name, fn = self._get_dir_fn(fn, is_write=True)
        data = text.encode()

        # azure fileservice has no append, so we need to cobble one together using FOUR API calls
        our_data_len = len(data)
        file_obj = self.fs.get_file_properties(self.share_name, dir_name, fn)
        total_length = file_obj.properties.content_length
        append_start = int(file_obj.metadata["append_length"])
        block_size = int(file_obj.metadata["block_size"])
        append_end = append_start + our_data_len
        #print("append_start=", append_start)

        if append_end > total_length:
            # extend size of file by adding another block
            print("extending size of file, new length={:,}".format(total_length + block_size))
            
            self.fs.resize_file(self.share_name, dir_name, fn, total_length + block_size)

        self.fs.set_file_metadata(self.share_name, dir_name, fn, 
            metadata={"append_length": str(append_end), "block_size": str(block_size)})

        return self.fs.update_range(self.share_name, dir_name, fn, data, append_start, append_end-1)

    def read_file(self, fn):
        dir_name, fn = self._get_dir_fn(fn, is_write=False)
        file_obj = self.fs.get_file_to_text(self.share_name, dir_name, fn)
        return file_obj.content

    def upload_file(self, store_path, source_fn):
        dir_name, fn = self._get_dir_fn(store_path, is_write=True)
        return self.fs.create_file_from_path(self.share_name, dir_name, fn, source_fn)

    def download_file(self, fn, dest_fn):
        dir_name, fn = self._get_dir_fn(fn, is_write=False)
        utils.ensure_dir_exists(file=dest_fn)
        #print("self.share_name=", self.share_name, ", dir_name=", dir_name, ", fn=", fn, ", dest_fn=", dest_fn)

        # supply friendly error msg for common cases
        if not self.fs.exists(self.share_name, dir_name, fn):
            utils.user_error("share file not found: {}".format(dir_name + "/" + fn))

        return self.fs.get_file_to_path(self.share_name, dir_name, fn, dest_fn)

    # def download_files(self, wildcard, dest_folder):
    #     path = self._expand_path(wildcard)
    #     return self.store._download_files(self.container, path, dest_folder)

    def get_filenames(self, wildcard="*", full_paths=False):
        #dir_name, fn = self._get_dir_fn(wildcard, is_write=False)
        if wildcard:
            dir_name = self.base_path + "/" + wildcard
        else:
            dir_name = self.base_path 
        fn = None
        #print("self.share_name=", self.share_name, ", dir_name=", dir_name, ", fn=", fn)

        generator = self.fs.list_directories_and_files(self.share_name, dir_name)  # , prefix=fn)
        names = [file_or_dir.name for file_or_dir in generator]
        files = []
        dirs = []

        for file_or_dir in generator:
            name = file_or_dir.name
            if self.fs.exists(self.share_name, directory_name=dir_name + "/" + name):
                dirs.append(name)
            else:
                files.append(name)

        return dirs, files

    def delete_files(self, wildcard):
        ''' NOTE: wildcards are not currently supported - only single filename can be deleted at a time.'''
        #path = self._expand_path(wildcard)
        dir_name, fn = self._get_dir_fn(wildcard, is_write=False)

        # supply friendly error msg for common cases
        if not self.fs.exists(self.share_name, dir_name, fn):
            utils.user_error("share file not found: {}".format(dir_name + "/" + fn))

        return self.fs.delete_file(self.share_name, dir_name, fn)

    def does_file_exist(self, fn):
        dir_name, fn = self._get_dir_fn(fn, is_write=False)
        #print("does_file_exist: fn=", fn, ", path=", path)
        return self.fs.exists(self.share_name, dir_name, fn)

class WorkspaceFiles(FilesObject):
    def __init__(self, store, ws_name):
        super(WorkspaceFiles, self).__init__(store, "workspaces", ws_name)

class RunFiles(FilesObject):
    def __init__(self, store, ws_name, run_name):
        super(RunFiles, self).__init__(store, "runs", ws_name + "." + run_name)

class ExperimentFiles(FilesObject):
    def __init__(self, store, ws_name, exper_name):
        super(ExperimentFiles, self).__init__(store, "experiments", ws_name + "." + exper_name)

class JobFiles(FilesObject):
    def __init__(self, store, job_name):
        super(JobFiles, self).__init__(store, "jobs", job_name)
