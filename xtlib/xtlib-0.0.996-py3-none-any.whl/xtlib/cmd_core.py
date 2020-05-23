# cmd_core.py: implements the commands used by XT command-line tool.
import os
import sys
import json
import time
import math
import shutil

from .helpers.bag import Bag
from . import utils as utils 
from .azure_batch import AzureBatch
from .client import Client
from . import app_information
from . import box_information
# constants
SH_NAME ="run.sh"

class CmdCore():

    def __init__(self, config, store, client, explicit_options):

        self.config = config
        self.store = store
        self.client = client

        # TODO: better mechanism for syncing these with client
        self.on_options_changed(explicit_options)

    def on_options_changed(self, explicit_options):
        self.explicit_options = explicit_options
        self.box = self.config.get("core", "box")
        self.ws = self.config.get("general", "workspace")
        utils.diagnostics = self.config.get("general", "diagnostics")

    def get_explicit_option(self, name):
        return self.explicit_options[name] if name in self.explicit_options else None

    def keygen(self, overwrite=False, fn=utils.LOCAL_KEYPAIR_PRIVATE):
        fn = os.path.expanduser(fn)

        # prevent "overwrite?" msg by first removing file
        if os.path.exists(fn):
            if overwrite:
                os.remove(fn)   
            else:
                utils.user_exit("existing key found (use --overwrite to force a new key to be generated)")

        # call ssh-keygen to do the GENERATION
        cmd = 'ssh-keygen -q -f "' + fn + '"'
        #print("keygen: cmd=", cmd)
        exit_code, output = utils.sync_run(cmd)
        if exit_code:
            print(output)
            return False

        # ensure ssh-agent is ENABLED
        cmd = "sc config ssh-agent start= demand"
        exit_code, output = utils.sync_run(cmd)
        if exit_code:
            print(output)
            return False

        # ensure ssh-agent is RUNNING
        cmd = "ssh-agent s"
        exit_code, output = utils.sync_run(cmd)
        if exit_code:
            print(output)
            return False

        # finally, ADD the generated key to the ssh repository
        cmd = 'ssh-add "{}"'.format(fn)
        #print("keygen: cmd=", cmd)
        exit_code, output = utils.sync_run(cmd)
        if exit_code:
            print(output)
            return False

        return True

    def keysend(self, box_name):
        box_addr = self.config.get("boxes", box_name, dict_key="address", default_value=box_name)
        box_os = self.config.get("boxes", box_name, dict_key="os", default_value="linux")

        #print("box_addr=", box_addr)
        fn_local_key = os.path.expanduser(utils.LOCAL_KEYPAIR_PUBLIC)
        #fn_log = utils.expand_vars(TEMP_SSH_LOG)

        if not os.path.exists(fn_local_key):
            utils.user_error("xt keypair not yet created; please run the 'xt keygen' command first")

        # copy the key to a temp file location on the box
        if box_os == "windows":
            temp_key_fn = "temp_key_file"
        else:
            temp_key_fn = "/tmp/temp_key_file"

        # NOTE: the "-o IdentitiesOnly=yes" option of is used to prevent the "too many authenication errors" problem 
        cmd = 'scp -o IdentitiesOnly=yes "{}" {}:{}'.format(fn_local_key, box_addr, temp_key_fn)
        utils.diag("  copying key file to box: cmd=" + cmd)

        # SCP COPY
        exit_code, output = utils.sync_run(cmd)
        if exit_code:
            print(output)
            return False

        # now, run commands on box to append the temp file to ~/.ssh/authorized_keys

        if box_os == "windows":
            AUTHORIZED_KEYS_FILE = ".ssh/authorized_keys"
            cmds = [
                "mkdir .ssh",    # ensure directory exists (if first key)
                "del {}".format(AUTHORIZED_KEYS_FILE),
                "type {} >> {}".format(temp_key_fn, AUTHORIZED_KEYS_FILE),   # append key to file
                "del {}".format(temp_key_fn)     # remove temp file
            ]
            cmdline = "&".join(cmds)
        else:
            AUTHORIZED_KEYS_FILE = "~/.ssh/authorized_keys"
            cmds = [
                "mkdir -p ~/.ssh",    # ensure directory exists (if first key)
                "cat {} >> {}".format(temp_key_fn, AUTHORIZED_KEYS_FILE),   # append key to file
                "rm {}".format(temp_key_fn)     # remove temp file
            ]
            cmdline = ";".join(cmds)

        # NOTE: the "-o IdentitiesOnly=yes" option of is used to prevent the "too many authenication errors" problem 
        cmd = 'ssh -o IdentitiesOnly=yes {} "{}"'.format(box_addr, cmdline)
        utils.diag("  running cmds on box=" + cmd)

        # SSH COMMANDS
        exit_code, output = utils.sync_run(cmd)
        if exit_code:
            print(output)
            return False

        return True

    def prep_for_azure_node(self, job, job_id, node_index, run_data_list, num_nodes, num_low_pri, using_hp, repeat, 
        tmp_dir, box_info, app_info, xtlib_capture):
        '''prepare runs for node node_index'''

        #print(f"AZURE-BATCH: running cmd: {user_cmd_parts}")
        box_name = job_id + "-box" + str(node_index) 
        
        fn_context, run_names = self.create_context_file(run_data_list, node_index, job_id, tmp_dir, using_hp, repeat, 
            box_info=box_info, app_info=app_info)

        hold_open = self.config.get("general", "hold")

        # this command runs the xt controller with a single job, described by the filename in fn_context
        xtc_command = "python -u -c \"from xtlib.controller import run as run; run({}, {}, '{}', {}, {})\" > controller.log" \
            .format(1, None, utils.FN_MULTI_RUN, hold_open, utils.CONTROLLER_PORT)  #  box_index+utils.AZURE_BATCH_BASE_CONTROLLER_PORT)

        # load prep script
        #app_info = self.get_app_info("xtlib/controller.py")
        #print("azure batch; controller app_info=", app_info)

        # if not app_info.app_class:
        #     utils.user_error("controller app is missing or has no 'app-class' property")

        # get prep script for XT controller
        controller_app_info = app_information.AppInfo(self.config, app_path="xtlib/controller.py", box_info=box_info)

        prep_script_cmds = controller_app_info.get_prep_script("combined")
        shell_launch_prefix = box_info.shell_launch_prefix

        add_cmds = [
            xtc_command, 
            "echo run_controller.sh it now exiting..."
        ]

        cmds = prep_script_cmds + add_cmds

        # use blob service from store 
        bs = self.store.helper.bs

        # put cmds into a shell script
        fn_sh = tmp_dir + "/" + SH_NAME 
        node_cmd = self.adjust_cmdline_for_script(cmds, fn_sh, SH_NAME, prefix=shell_launch_prefix)
        #print("calling launch: cmds=", cmds)

        # build RESOURCE FILES for each file we have uploaded into "before" directory
        before_path = "node-{}/before".format(node_index)
        after_path = "node-{}/after".format(node_index)

        # UPLOAD input files for running xt controller to BEFORE dir of job (2 files, both begin with xtc_*)
        local_file_names = [fn_context, fn_sh]
        self.store.upload_files_to_job(job_id, before_path, tmp_dir + "/*")

        before_blob_path = utils.path_join(utils.JOBS_DIR, job_id, before_path)
        blob_names = [blob.name for blob in bs.list_blobs(utils.INFO_CONTAINER, before_blob_path)]
        #blob_names = [before_blob_path]

        # for the DEST FILENAME on the node, strip off the blob path prefix
        bbp_len = 1 + len(before_blob_path)    # +1 to remove the trailing "/"
        node_file_names = [ bn[bbp_len:] for bn in blob_names ]

        if xtlib_capture:
            xtlib_blob_path = utils.path_join(utils.JOBS_DIR, job_id, "ExperimentTools", "xtlib")

            # @rfernand - 8/11/2019: cannot get ResourceFile with partial blob name to download all files at once
            # so changed code to enumerate each file 
            use_partial_blobname = False
            if use_partial_blobname:
                local_file_names.append("xtlib")     # debugging help only (not actual path)
                blob_names.append(xtlib_blob_path)
                
                node_file_names.append("./ExperimentTools/xtlib")
            else:
                xtlib_root = "ExperimentTools/xtlib/"
                xtlib_blob_names = self.store.get_job_filenames(job_id, xtlib_root + "**", full_paths=True)  
                blob_names += xtlib_blob_names

                root_len = 1 + len(utils.path_join(utils.JOBS_DIR, job_id))
                node_file_names += [ bn[root_len:] for bn in xtlib_blob_names ]

        utils.diag("  local_file_names=" + str(local_file_names))
        utils.diag("  files uploaded to blobs: " + str(blob_names))
        utils.diag("  node_file_names=" + str(node_file_names))

        # use our helper to convert blobs and filenames to resource files
        node_res_files = job.convert_blobs_to_resource_files(utils.INFO_CONTAINER, blob_names, node_file_names)

        # convert OUTPUT WILDCARDS to output files
        output_file_list = ["controller.log", "../*.txt"]

        after_blob_path = utils.JOBS_DIR + "/" + job_id + "/" + after_path
        node_output_files = job.build_output_files(utils.INFO_CONTAINER, after_blob_path, output_file_list)
        #print("outfile_names=", output_file_list)
        #print("output_files=", output_files)

        if True:  # num_nodes > 1:
            utils.feedback("  box: {}, run(s): {}".format(box_name.upper(), run_names.upper()), is_final=True)
        else:
            utils.feedback("box: {}, run(s): {}".format(box_name.upper(), run_names.upper()), is_final=True)

        return {"node_cmd": node_cmd, "node_res_files": node_res_files, "node_output_files": node_output_files}

    def run_azure_job(self, job_id, run_data_list_by_node, pool_info, using_hp, repeat, box_info, app_info, 
        xtlib_capture, is_distributed):
        '''
        This runs the controller on one or more boxes within an Azure Batch pool.
        '''

        #print("pool_info=", pool_info)
        vm_size = pool_info["vm-size"]
        vm_image = pool_info["vm-image"]
        num_nodes = pool_info["nodes"]
        num_low_pri = pool_info["low-pri"]
        
        utils.feedback("azure-batch (vm_size={}, vm_image={}, num_nodes={}, low_pri={})".format(vm_size, vm_image, 
            num_nodes, num_low_pri), is_final=True)

        ws_name = self.ws
        job = AzureBatch(config=self.config)

        if self.config.get("core", "store-type") != "azure-store":
            raise Exception("Can only run Azure Batch with 'azure-store' store service")

        #print("len(run_data_list_by_node)=", len(run_data_list_by_node))

        # first, build a list of runs for each node in our azure batch pool
        node_records = []
        tmp_dirs = []

        for n, run_data_list in enumerate(run_data_list_by_node):

            # create a temp directory for file (ensure it is empty)
            tmp_dir = utils.make_tmp_dir("run-azure-batch-node{}-".format(n), False)
            tmp_dirs.append(tmp_dir)

            node_record = self.prep_for_azure_node(job, job_id, n, run_data_list, num_nodes, num_low_pri, 
                using_hp=using_hp, repeat=repeat, tmp_dir=tmp_dir, box_info=box_info, app_info=app_info, 
                xtlib_capture=xtlib_capture)
            node_records.append(node_record)

        # "hold" is now used to hold open the xt controller task AND the created pool
        auto_pool = not self.config.get("general", "hold")

        # finally, launch the job on AZURE BATCH
        pool_id = job.launch(job_id, node_records, auto_pool=auto_pool, ws_name=ws_name, vm_size=vm_size, 
            vm_image=vm_image, num_nodes=num_nodes, num_low_pri=num_low_pri, is_distributed=is_distributed)

        utils.feedback("job submitted", is_final=True)

        #self.attach_task_to_console(ws_name, run_name, job_id=job_id)

        # clean up tmp_dirs
        for tmp_dir in tmp_dirs:
            shutil.rmtree(tmp_dir)

    def get_ip_addr_from_box_addr(self, box_addr):
        ip_addr = None

        if box_addr:
            if "@" in box_addr:
                ip_addr = box_addr.split("@")[1]
            else:
                ip_addr = box_addr
        return ip_addr

    def kill_runs_by_job(self, job_id):
        kill_results_by_boxes = {}

        if not str(job_id).startswith("job"):
            utils.user_error("not a valid job id: " + str(job_id))

        #print("job_id=", job_id)
        text = self.store.read_job_info_file(job_id)
        job_info = json.loads(text)
        runs_by_box = job_info["runs_by_box"]
        #print("runs_by_box=", runs_by_box)

        pool_info = job_info["pool_info"]
        if utils.dict_default(pool_info, "service") == "azure-batch":
            # azure-batch job
            azure_batch = AzureBatch(self.config)

            for node_index, (box_name, runs) in enumerate(runs_by_box.items()):
                ws, run_name = runs[0].split("/")

                ### it turns out to be better to avoid connecting with the controller 
                ### when we are about to kill the controller (avoid thread 2 exception).
                ### besides, it's also better to kill as quickly as possible and then clean
                ### up the runs that need it.

                # always kill the job's node at the azure batch service level
                kill_records, pool_id = azure_batch.kill_job_node(self.store, job_id, node_index, runs)
                #print("kill_records from azure_batch_kill=", kill_records)

                # if not kill_records:
                #     kill_records = kill_records2
                kill_results_by_boxes[box_name] = kill_records
                #print("kill_results_by_boxes=", kill_results_by_boxes)

            # now kill the job itself
            azure_batch.kill_job(self.store, job_id)
        else:
            # traditional boxes
            for box_name, runs in runs_by_box.items():
                self.client.change_box(box_name, True)
                #print("box_name=", box_name, ", run_names=", runs)

                kill_records = self.client.kill_runs(runs)
                kill_results_by_boxes[box_name] = kill_records

        return kill_results_by_boxes

    def kill_runs_by_boxes(self, runs_by_box):
        kill_results_by_boxes = {}

        for box_name, run_names in runs_by_box.items():
            kill_results = None

            # connect to specified box
            self.client.change_box(box_name, True)

            try:
                if utils.is_azure_batch_box(box_name):
                    job_id, bpart = box_name.split("-")
                    node_index = bpart[3:]     # strip off the "box" at the beginning
                    azure_batch = AzureBatch(self.config)
                    kill_results, _ = azure_batch.kill_job_node(self.store, job_id, node_index, run_names)
                else:
                    kill_results = self.client.kill_runs(run_names)
            except Exception as ex:
                utils.report_exception(ex)
                pass

            kill_results_by_boxes[box_name] = kill_results

        return kill_results_by_boxes

    def adjust_cmdline_for_script(self, cmd, local_script_fn, node_script_fn, prefix=None):
        #cmd = "PATH=\$HOME/bin:\$PATH\ && " + cmd       # add path due to how we are launced
        #cmd = '/bin/bash -c "' + cmd + '"'              # wrap as a bash command due to how we are launched
        if isinstance(cmd, (list, tuple)):
            if local_script_fn:

                # write SCRIPT file
                # must specify newline="" to avoid CR char being inserted (which linux cannot handle)
                with open(local_script_fn, "wt", newline='') as tfile:
                    tfile.write("\n".join(cmd))
                
                #input_files.append("before/" + script_fn)

                # sudo needed for "conda update" (bug on their part)
                # "--login" option allow commands to run normally (as if executed interactively)
                if prefix == None:
                    prefix = "sudo -A sh --login"
                cmd = prefix + " " + node_script_fn
            else:
                cmd = " && ".join(cmd)

        #print("final cmd: ", cmd, ", input_files=", input_files, sep="")
        return cmd

    def get_runs_by_box(self, full_run_names):
        runs_by_box = {}

        for full_run_name in full_run_names:
            # get box_name of run
            ws, run_name = full_run_name.split("/")
            records = self.store.get_run_log(ws, run_name)
            box_name = records[0]["data"]["box_name"]

            # add to dict of lists
            if not box_name in runs_by_box:
                runs_by_box[box_name] = []

            runs_by_box[box_name].append(full_run_name)

        return runs_by_box

    def create_context_file(self, run_data_list, node_index, job_id, tmp_dir, using_hp, repeat, 
        app_info, box_info):
        ''' create a "node context" JSON file describing all of the runs we need to do for the 
        current node.  the xt controller will use this file to queue up all of the
        runs when it starts.
        '''
        node_runs = []
        node_context = {"job_id": job_id, "node_index": node_index, "runs": node_runs}
        run_names = ""

        for run_data in run_data_list:

            cmd_parts = run_data["cmd_parts"]
            run_name = run_data["run_name"]
            box_name = run_data["box_name"]

            #exper_name, app_name, app_info = self.get_exper_name(cmd_parts)
            exper_name = app_info.exper_name
            app_name = app_info.app_name

            # build the context for this run
            run_context = self.get_client_context(exper_name, run_name, app_info, box_info, 
                node_index=node_index, job_id=job_id, cmd_parts=cmd_parts, using_hp=using_hp, repeat=repeat)

            run_context.cmd_parts = cmd_parts
            run_context = run_context.__dict__

            node_runs.append(run_context)
            if run_names == "":
                run_names = run_name
            else:
                run_names += ", " + run_name
        
        fn_context = tmp_dir + "/" + utils.FN_MULTI_RUN 
        text = json.dumps(node_context)
        with open(fn_context, "wt") as tfile:
            tfile.write(text)

        return fn_context, run_names

    def get_client_context(self, exper_name, run_name, app_info, box_info, 
            job_id, node_index, cmd_parts, resume_name=None, using_hp=False, repeat=None):
        config = self.config
        context = Bag()

        context.ws = self.ws
        context.exper_name = exper_name
        context.run_name = run_name
        context.job_id = job_id
        context.app_name = app_info.app_name
        context.box = self.box
        context.from_ip = utils.get_ip_address()
        context.from_host = utils.get_hostname()
        context.box_name = box_info.box_name
        context.target_file = self.get_target(cmd_parts)
        context.resume_name = resume_name

        # for helping docker login to user's Azure Container Registry
        is_docker = (cmd_parts[0] == "docker") or (cmd_parts[0] == "sudo" and cmd_parts[1] == "docker")
        needs_login = is_docker and config.get("azure-container-registry", "login")

        context.docker_login = needs_login
        if needs_login:
            context.docker_server = config.get("azure-container-registry", "login-server")
            context.docker_username = config.get("azure-container-registry", "username")
            context.docker_password = config.get("azure-container-registry", "password")

        # config info
        #box_os = self.get_box_os(box_name)
        box_os = box_info.box_os
  
        before_files_list = self.config.get("general", "before-files") 
        # allow user to use a simple string
        if isinstance(before_files_list, str):
            before_files_list = [ before_files_list ]

        after_files_list = self.config.get("general", "after-files")
        # allow user to use a simple string
        if isinstance(after_files_list, str):
            after_files_list = [ after_files_list ]

        context.before_files_list = before_files_list
        context.after_files_list = after_files_list

        context.metric_rollup_dict = config.get("metrics", None)
        context.capture = config.get("general", "capture")
        context.scrape = config.get("general", "scrape")
        context.log = config.get("general", "log")
        context.repeat = repeat
        context.repeats_remaining = None      # will be set in controller
        context.restart = False
        context.max_runs = config.get("general", "max-runs")
        context.xtlib_capture = self.config.get("general", "xtlib-capture")

        hp_config = config.get("general", "hp-config")
        if hp_config:
            hp_config = utils.path_join(utils.HP_CONFIG_DIR, os.path.basename(hp_config))

        context.hp_config = hp_config
        context.using_hp = using_hp
        context.arg_prefix = config.get("hp-search", "arg-prefix")
        context.aggregate_dest = config.get("hp-search", "aggregate-dest")
        context.dest_name = exper_name if context.aggregate_dest == "experiment" else job_id
        context.aggregate_dest = self.config.get("hp-search", "aggregate-dest")

        store_type = config.get("core", "store-type")
        context.store_type = store_type

        if store_type == "file-store":
            # import to expand things like "${HOME}" now, since controller is not running as a particular user
            context.store_path = utils.expand_vars(config.get("core", "file-store-path"))
            context.store_key = None
        elif store_type == "azure-store":
            context.store_path = config.get("azure", "storage-name")
            context.store_key = config.get("azure", "storage-key")
        else:
            raise Exception("unsupported store found in config file: " + store_type)

        # prep scripts
        #print("context.repeat=", context.repeat)

        # TODO: add other conditions that make this run a parent (sweep file without repeat?)
        context.is_parent = context.repeat

        if context.is_parent:
            # get parent/child versions
            #parent_prep_script, shell_launch_prefix = self.get_prep_script(app_info, box_name, "parent")
            parent_prep_script = app_info.get_prep_script("parent")
            child_prep_script = app_info.get_prep_script("child")

            context.parent_prep_script = parent_prep_script
            context.child_prep_script = child_prep_script
            context.prep_script = None
        else:
            # get combined version
            prep_script = app_info.get_prep_script("combined")

            context.prep_script = prep_script
            context.parent_prep_script = None
            context.child_prep_script = None

        context.shell_launch_prefix = box_info.shell_launch_prefix
        
        box_name, pool = box_information.get_service_params(self.config, job_id, box_info.box_name, node_index)
        context.job_id = job_id
        context.pool = pool
        context.node_index = node_index

        #print("context=", context)
        return context

    def get_fn_run(self, args):
        # find first non-option at end of cmd to mark end of "fn_run"
        fn_run = ""

        #print("get_fn_run: args=", args)
        if not args:
            utils.internal_error("get_fn_run: args cannot be empty")

        if len(args) >= 2:
            if args[0] == "run":
                fn_run = os.path.abspath(args[1])
            elif args[0] == "python":
                # skip over python options
                index = 1
                while index < len(args) and args[index].startswith("-"):
                    index += 1
                if index < len(args):
                    fn_run = os.path.abspath(args[index])

        #print("fn_run=", fn_run)
        return fn_run

    def list_store_files(self, ws, path, subdirs):
        files = self.store.list_files(ws, path, subdirs)
        return files

    def get_target(self, cmd_parts):
        target = None

        if cmd_parts:
            if cmd_parts[0] == "python":
                cmd_parts = cmd_parts[1:]
            elif cmd_parts[0] == "docker":
                cmd_parts = cmd_parts[1:]
                if cmd_parts[0] == "run":
                    cmd_parts = cmd_parts[1:]
    
            for arg in cmd_parts:
                if not arg.startswith("-"):
                    target = arg
                    break

        return target

    def docker_login(self, server, username, password):
        exit_code, output = utils.sync_run(["docker", "login", server, "--username", username, "--password", password],  capture_output=True, shell=False, report_error=True)
        return output

    def docker_logout(self, server):
        exit_code, output = utils.sync_run(["docker", "logout", server],  capture_output=True, shell=False, report_error=True)
        return output

    def upload_xtlib_to_job(self, job_id, job_path):
        copied_files = None

        # get path to xtlib from PYTHONPATH env variable
        path_str = os.getenv("PYTHONPATH")
        if path_str:
            path_list = path_str.split(";")
            xt_dir = "ExperimentTools"
            paths = [p for p in path_list if xt_dir.lower() in p.lower()]
            if paths:
                local_path = utils.path_join(paths[0], "xtlib", "*")
                #print("local_path=", local_path)
                copied_files = self.store.upload_files_to_job(job_id, job_path, local_path, recursive=True, 
                    exclude_dirs_and_files=["__pycache__"])
                utils.feedback("{} xtlib files uploaded to job".format(len(copied_files)))

        if not copied_files:
            utils.user_errror("could not find {} directory in PYTHONPATH: {}".format(xt_dir, path_str))
          
        return local_path

    def run_request(self, cmd_parts, using_hp, resume_name, keep_name, demand_mode, cmds_by_node, sweep_text):

        # create the job to hold all runs
        job_id = self.store.create_job()

        # write to job-level sweeps-list file
        #print("cmds_by_node=", cmds_by_node)   
        if cmds_by_node:
            cmds_by_node_text = json.dumps(cmds_by_node)
            self.store.create_job_file(job_id, utils.HP_SWEEP_LIST_FN, cmds_by_node_text)

        boxes, pool_info, is_auzre_pool, is_azure_box = box_information.get_box_list(self, job_id=job_id)
        num_boxes = len(boxes)

        is_distributed = self.config.get("general", "distributed")
        if is_distributed:
            # check for conflicts
            if using_hp:
                utils.user_error("Cannot do hyperparamer search on a distributed-training job")
            if not is_auzre_pool:
                utils.user_error("Distributed-training is currently only supported for azure pool jobs")

        utils.feedback("job: " + job_id.upper())
        path =  self.get_target(cmd_parts)
        path = os.path.abspath(path)        # fully qualify path
        #print("path=", path)
        
        first_box_info = box_information.BoxInfo(self.config, boxes[0])
        first_app_info = app_information.AppInfo(self.config, path, first_box_info)

        app_name = first_app_info.app_name

        if num_boxes > 1 and not is_auzre_pool:
            utils.feedback("app: " + app_name, is_final=True)
        else:
            utils.feedback("app: " + app_name)

        run_data_list_by_box = []
        parent_name = None
        run_data_list_by_node = []

        if using_hp:
            # CAPTURE BEFORE files to JOB
            local_file_names = self.capture_before_files(run_name=None, rerun_name=resume_name, use_job_id=job_id)

        xtlib_capture = self.config.get("general", "xtlib-capture")
        if xtlib_capture:
            self.upload_xtlib_to_job(job_id, "ExperimentTools/xtlib")

        # BOX LOOP: create a run for each box
        for i, box_name in enumerate(boxes):  
            repeat_count = self.config.get("general", "repeat")
            #print("repeat_count from config=", repeat_count, ", using_hp=", using_hp)

            box_info = box_information.BoxInfo(self.config, box_name)
            app_info = app_information.AppInfo(self.config, path, box_info)

            # get EXPER_NAME
            # exper_name, app_name, app_info = self.get_exper_name(cmd_parts)
            # if not exper_name:
            #     exper_name = input("experiment name (for grouping this run): ")
            exper_name = app_info.exper_name
            app_name = app_info.app_name
        
            # do we need to override "repeat"?
            node_id = "node" + str(i)
            if using_hp:
                if node_id in cmds_by_node:
                    repeat_count = len(cmds_by_node[node_id])
                    #print("repeat_count override=", repeat_count)

            actual_parts = list(cmd_parts)
            if box_info.box_os == "linux" and actual_parts[0] == "docker":
                # give our user permission to run DOCKER on linux
                actual_parts.insert(0, "sudo")
            #print("actual_parts=", actual_parts)

            # CREATE RUN and UPLOAD files
            run_name, full_run_name, box_name, pool = \
                self.create_run(job_id, actual_parts, box_name=box_name, parent_name=parent_name, node_index=i, using_hp=using_hp, 
                    repeat=repeat_count, app_info=app_info, path=path)

            run_data = {"run_name": run_name, "cmd_parts": actual_parts, "box_name": box_name}
            run_data_list = [run_data]
            run_data_list_by_box.append(run_data_list)
            # #print("run_data_list=", run_data_list)

            # do this ONCE (before run_job_on_box is called)
            if i == 0:
                self.upload_sweep_data(sweep_text, exper_name, job_id)

            # run the job
            if is_auzre_pool:
                run_data_list_by_node.append(run_data_list)
            else:
                if len(boxes) > 1:
                    utils.feedback(f"  box: {box_name.upper()}")  
                else:
                    utils.feedback(f"box: {box_name.upper()}")  
        
                self.client.run_job_on_box(job_id, run_data_list, box_index=i, box_info=box_info, app_info=app_info, 
                    pool_info=pool_info,  resume_name=resume_name, demand_mode=demand_mode, repeat=repeat_count, 
                    using_hp=using_hp)
    
        if is_auzre_pool:
            # create and start an azure batch job for all of the "run_data_list_by_node"
            #print("run_data_list_by_node=", run_data_list_by_node)
            
            self.run_azure_job(job_id, run_data_list_by_node, pool_info, using_hp=using_hp, repeat=repeat_count, 
                box_info=first_box_info, app_info=first_app_info, xtlib_capture=xtlib_capture, is_distributed=is_distributed)
    
        # log job info 
        runs_by_box = {}
        for i, run_data_list in enumerate(run_data_list_by_node):
            for rd in run_data_list:   
                box_name = rd["box_name"]
                if not box_name in runs_by_box:
                    runs_by_box[box_name] = [] 
                    full_run_name = self.ws + "/" + rd["run_name"]
                runs_by_box[box_name].append(full_run_name)

        self.store.log_job_info(job_id, pool_info, runs_by_box)

        return run_data_list_by_box
        
    def upload_sweep_data(self, sweep_text, exper_name, job_id):
        # upload SWEEP file to job or experiment directory
        fn_sweeps = self.config.get("general", "hp-config")
        agg_dest = self.config.get("hp-search", "aggregate-dest")

        if fn_sweeps:
            if not os.path.isfile(fn_sweeps):
                utils.user_error("specified APP-CONFIG file not found: " + str(fn_sweeps))
            
            # upload to a known folder name (since value of fn_sweeps can vary) and we need to find it later
            target_name = utils.path_join(utils.HP_CONFIG_DIR, os.path.basename(fn_sweeps))
            
            if agg_dest == "experiment":
                self.store.upload_file_to_experiment(self.ws, exper_name, target_name, fn_sweeps)
            else:
                self.store.upload_file_to_job(job_id, target_name, fn_sweeps)
        elif sweep_text:
            # be consistent: store under hp-config
            target_name = utils.path_join(utils.HP_CONFIG_DIR, utils.HP_CONFIG_FN)

            # upload cmdline-GENERATED SWEEPS file to experiment/job
            #print("sweep_text=", sweep_text)

            if agg_dest == "experiment":
                self.store.create_experiment_file(self.ws, exper_name, target_name, sweep_text)
            else:
                self.store.create_job_file(job_id, target_name, sweep_text)
                        
    def create_run(self, job_id, user_cmd_parts, box_name="local", parent_name=None, rerun_name=None, node_index=0, 
            using_hp=False, repeat=None, app_info=None, path=None):
        '''
        'create_run' does the following:
            - creates a new run name (and matching run directory in the store)
            - logs a "created" record in the run log
            - logs a "created" record in the workspace summary log
            - logs a "cmd" record in the run log
            - log an optional "notes" record in the run log
            - captures the run's "before" files to the store's run directory

        '''
        utils.timing("create_run: start")

        box_name, pool = box_information.get_service_params(self.config, job_id, box_name, node_index)
        #exper_name, app_name, app_info = self.get_exper_name(user_cmd_parts)
        exper_name = app_info.exper_name
        app_name = app_info.app_name

        run_name = ""
        log_to_store = self.config.get("general", "log")
        aggregate_dest = self.config.get("hp-search", "aggregate-dest")

        if log_to_store:
            if not exper_name:
                exper_name = input("experiment name (for grouping this run): ")

            #print("calling store.start_run with exper_name=", exper_name)
            username = self.config.get("core", "username")
            description = self.config.get("general", "description")

            utils.timing("create_run: before start_run")

            # create RUN in store
            if parent_name:
                run_name = self.store.start_child_run(self.ws, parent_name, box_name=box_name, username=username,
                    exper_name=exper_name, app_name=app_name, pool=pool, job_id=job_id, node_index=node_index, 
                    description=description, aggregate_dest=aggregate_des, path=path)
            else:
                run_name = self.store.start_run(self.ws, exper_name=exper_name, box_name=box_name, app_name=app_name, 
                    username=username, repeat=repeat, pool=pool, job_id=job_id, node_index=node_index, 
                    description=description, aggregate_dest=aggregate_dest, path=path)

            utils.timing("create_run: after start_run")

            # log CMD record
            self.store.log_run_event(self.ws, run_name, "cmd", {"cmd": user_cmd_parts})

            store_type = self.config.get("core", "store-type")
            full_run_name = utils.format_workspace_exper_run(store_type, self.ws, exper_name, run_name)

            # log NOTES record
            if self.config.get("general", "notes") in ["before", "all"]:
                text = input("Notes: ")
                if text:
                    self.store.log_run_event(self.ws, run_name, "notes", {"notes": text})
        else:
            full_run_name = ""

        utils.timing("create_run: after logging")

        # capture BEFORE files (must be done on originating client for access to local files)
        if not parent_name:
            if rerun_name:
                utils.diag("  capturing BEFORE files from rerun: {}".format(rerun_name))
            else:
                utils.diag("  capturing BEFORE files from LOCAL DIR")

            if using_hp:
                # before files were captures to the job store
                pass
            else:
                local_file_names = self.capture_before_files(run_name, rerun_name=rerun_name)
                utils.diag("  captured {} files".format(len(local_file_names)))

        utils.timing("create_run: after capture")

        return run_name, full_run_name, box_name, pool

    def capture_before_files(self, run_name, preserve_run_sh=False, extra_files = [], rerun_name=None, use_job_id=None):
        copied_files = []

        if self.config.get("general", "capture") in ["before", "all"]:
            started = time.time()

            if rerun_name:
                if "/" in rerun_name:
                    ws, rerun_name = rerun_name.split("/")
                    
                copied_files = self.store.copy_run_files_to_run(self.ws, rerun_name, "before/", run_name, "before")
            else:
                # minimize confusion by deleting known files form previous run output
                utils.zap_file("console.txt")

                if not preserve_run_sh:
                    utils.zap_file(SH_NAME)

                # CAPTURE user-specified INPUT FILES
                before_files_list = self.config.get("general", "before-files") 
                # allow user to use a simple string
                if isinstance(before_files_list, str):
                    before_files_list = [ before_files_list ]
                before_files_list += extra_files
                
                omit_list = self.config.get("general", "omit") 
                
                for input_files in before_files_list:
                    if use_job_id:
                        # "input_files" is a wildcard string relative to the current working directory
                        copied_files += self.store.upload_files_to_job(use_job_id, "before", input_files, exclude_dirs_and_files=omit_list)
                        dest_name = "job"
                        elapsed = time.time() - started
                        self.store.log_job_event(use_job_id, "capture_before", {"elapsed": elapsed, "count": len(copied_files)})
                    else:
                        # "input_files" is a wildcard string relative to the current working directory
                        copied_files += self.store.upload_files_to_run(self.ws, run_name, "before", input_files, exclude_dirs_and_files=omit_list)
                        dest_name = "run"
                        elapsed = time.time() - started
                        self.store.log_run_event(self.ws, run_name, "capture_before", {"elapsed": elapsed, "count": len(copied_files)})


            utils.feedback("{} target file(s) uploaded to {}".format(len(copied_files), dest_name))

        return copied_files


