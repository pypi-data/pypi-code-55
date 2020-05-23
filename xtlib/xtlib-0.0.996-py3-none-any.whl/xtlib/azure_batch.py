# azure_batch.py: support for running a XT job on a 1-N Azure Batch Compute boxes.

import os
import io
import sys
import time
import datetime
import numpy as np

import azure.storage.blob as azureblob
import azure.batch.models as batchmodels
import azure.batch.batch_auth as batch_auth
import azure.batch.batch_service_client as batch
# CAUTION: "batchmodels" is NOT the same as batch.models

from .helpers.xt_config import XTConfig
from .helpers.key_press_checker import KeyPressChecker
from . import utils

class AzureBatch():
    ''' for now, KISS:
        - single task
    '''

    def __init__(self, config=None):
        if config is None:
            config = read_config()

        self.config = config
        store_name = self.config.get("azure", "storage-name")
        store_key = self.config.get("azure", "storage-key")

        blob_client = azureblob.BlockBlobService(account_name=store_name, account_key=store_key)
        blob_client.retry = utils.make_retry_func()
        self.blob_client = blob_client
        self.batch_client = None
        #print("blob_client=", blob_client)

    def launch(self, job_id, node_records, auto_pool=True, description=None, ws_name=None, 
            vm_size=None, vm_image=None, num_nodes=1, num_low_pri=0, is_distributed=False):
        
        # self.cmd_line = command
        # self.resource_files = resource_files
        # self.output_files = output_files
        #self.run_name = run_name

        self.auto_pool = auto_pool
        self.description = description

        self.ws_name = ws_name
        self.job_id = job_id
        self.pool_id = "__pool" + utils.get_num_from_job_id(job_id) + "__"
        #print("pool_id=", self.pool_id + ", job_id=", self.job_id)

        self.vm_size = vm_size
        self.azure_image = vm_image 
        self.num_nodes = num_nodes 
        self.num_low_pri = num_low_pri 

        self.start_time = datetime.datetime.now().replace(microsecond=0)

        self.create_batch_client()

        # create our pool and job together 
        self.create_pool_and_job(is_distributed)
        
        # add the specified tasks (commands) to our job
        self.add_tasks_to_job(node_records)

        # job is now launced (usually remained queued for 2-4 minutes, then starts running)
        return self.pool_id      # may have changed (for auto_pool=True, the default)

    def create_batch_client(self):
        # create a batch_client to handle most of our azure needs
        batch_name = self.config.get("azure", "batch-name")
        batch_key = self.config.get("azure", "batch-key")
        batch_url = self.config.get("azure", "batch-url")

        if not batch_name or batch_name.startswith("xxxx"):
            utils.user_error("'batch-name' must be set in [azure] section of XT config file")

        if not batch_key or batch_key.startswith("xxxx"):
            utils.user_error("'batch-key' must be set in [azure] section of XT config file")

        if not batch_url or batch_url.startswith("xxxx"):
            utils.user_error("'batch-url' must be set in [azure] section of XT config file")
    
        credentials = batch_auth.SharedKeyCredentials(batch_name, batch_key)
        batch_client = batch.BatchServiceClient(credentials, batch_url= batch_url)
        
        batch_client.retry = utils.make_retry_func()
        self.batch_client = batch_client

    def get_azure_box_addr(self, job_id, node_index):
        ip_addr = None
        port = None
        state = None

        if not self.batch_client:
            self.create_batch_client()

        # XT always has exactly 1 task running on each node (xt controller), so
        # we can reply on task[x] running on node index x
        task_id = "task" + str(node_index)
        task = self.batch_client.task.get(job_id, task_id)

        state = task.state
        if state in ["running", "completed"]:
            node_info = task.node_info
            pool_id = node_info.pool_id
            node_id = node_info.node_id

            try:
                #print("job_id=", job_id, ", pool_id=", pool_id, ", mode_id=", node_id)
                node = self.batch_client.compute_node.get(pool_id, node_id)
                #print("node.ip_address=", node.ip_address)

                for ep in node.endpoint_configuration.inbound_endpoints:
                    if ep.name.startswith("xt-controller"):
                        # found our address for the specified node_index
                        ip_addr = ep.public_ip_address
                        port = ep.frontend_port
                        break
            except BaseException as ex:
                # treat any exception here as the pool being deallocated
                pass

        return state, ip_addr, port

    def wait_for_job_completion(self, max_wait_minutes=60):
        # Pause execution until tasks reach Completed state.
        completed = self.wait_for_tasks_to_complete()

    def create_network_config(self):
        '''open port CONTROLLER_PORT for incoming traffic on all nodes in pool '''
        rules = network_security_group_rules=[
                batchmodels.NetworkSecurityGroupRule(priority=179, access=batchmodels.NetworkSecurityGroupRuleAccess.allow,
                    source_address_prefix='*')
            ]

        nat_pools = [
            batchmodels.InboundNATPool(
                name='xt-controller-rpc',
                protocol='tcp', 
                # NOTE: client machine should connect to the Azure Batch app using the port that is dynamically ASSIGNED 
                # to the node (node_index + AZURE_BATCH_BASE_CONTROLLER_PORT).
                # Note: Azure Batch node should listen via the CONTROLLER_PORT
                backend_port=utils.CONTROLLER_PORT,   
                frontend_port_range_start=utils.AZURE_BATCH_BASE_CONTROLLER_PORT, 
                frontend_port_range_end=500 + utils.AZURE_BATCH_BASE_CONTROLLER_PORT,
                network_security_group_rules=rules),
        ]

        pep_config = batchmodels.PoolEndpointConfiguration(inbound_nat_pools=nat_pools)
        network_config = batchmodels.NetworkConfiguration(endpoint_configuration=pep_config)

        return network_config

    def create_pool_and_job(self, is_distributed):
        props = self.config.get("azure-images", self.azure_image)
        if not props:
            utils.user_error("No config file entry found in [azure-images] section for azure-image=" + self.azure_image)

        publisher = props["publisher"]
        offer = props["offer"]
        sku = props["sku"]
        version = props["version"]
        node_agent_sku_id = props["node-agent-sku-id"]

        # print(f"\npublisher={publisher}, offer={offer}, sku={sku}, node-agent-sku-id={node_agent_sku_id}, vm_size={self.vm_size}")
        # print("vm-image=", self.azure_image, ", props=", props)

        img_ref = batchmodels.ImageReference(publisher=publisher, offer=offer, sku=sku, version=version)
        vmc = batchmodels.VirtualMachineConfiguration(image_reference=img_ref, node_agent_sku_id=node_agent_sku_id)

        network_config = self.create_network_config()

        max_tasks_per_node = None
        enable_inter_node_communication = False

        if is_distributed:
            max_tasks_per_node = 1
            enable_inter_node_communication = True

        if self.auto_pool:
            # create a dynamically allocated pool
            pool_spec = batch.models.PoolSpecification(
                #id=self.pool_id,
                virtual_machine_configuration=vmc,
                vm_size=self.vm_size,
                network_configuration=network_config,
                target_dedicated_nodes=self.num_nodes,
                target_low_priority_nodes=self.num_low_pri,
                max_tasks_per_node = max_tasks_per_node,
                enable_inter_node_communication=enable_inter_node_communication)

            auto_pool = batch.models.AutoPoolSpecification(pool_lifetime_option="job", keep_alive=False, pool=pool_spec)
            pool_info = batch.models.PoolInformation(auto_pool_specification= auto_pool)
        else:
            # create a statically allocated pool
            #print(f'Creating pool [{self.pool_id}]...')
            new_pool = batch.models.PoolAddParameter(id=self.pool_id,
                virtual_machine_configuration=vmc,
                vm_size=self.vm_size,
                network_configuration=network_config,
                target_dedicated_nodes=self.num_nodes,
                target_low_priority_nodes=self.num_low_pri,
                max_tasks_per_node = max_tasks_per_node,
                enable_inter_node_communication=enable_inter_node_communication)

            # if is_distributed:
            #     new_pool.inter_compute_node_communication_enabled = True
            #     new_pool.max_tasks_per_compute_node = 1

            self.batch_client.pool.add(new_pool)
            pool_info = batch.models.PoolInformation(pool_id=self.pool_id)  # , auto_pool_specification= auto_pool)

        # CREATE THE JOB (but doesn't launch it yet)
        job = batch.models.JobAddParameter(id=self.job_id, pool_info=pool_info, 
            on_all_tasks_complete="terminateJob")

        self.batch_client.job.add(job)
        self.job = job

    def get_elevated_user_identify(self):
        aus = batchmodels.AutoUserSpecification(elevation_level=batchmodels.ElevationLevel.admin, 
            scope=batchmodels.AutoUserScope.task)
        user = batchmodels.UserIdentity(auto_user=aus)
        return user

    def delete_container_if_exists(self, name):
        if self.blob_client.exists(name):
            self.blob_client.delete_container(name)

    def get_outfiles_container_url(self, dest_container_name):
        # TODO - move OutputFiles code into AzureLaunchTest and xt_client
        # create container to hold output files
        
        self.blob_client.create_container(dest_container_name, fail_on_exist=False)

        # create an SAS for writing to the container
        sas_token = self.blob_client.generate_container_shared_access_signature(dest_container_name, 
            permission=azureblob.ContainerPermissions.WRITE,
            expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=24))

        # secret trick: construct SAS URL for the container
        storage_name = self.config.get("azure", "storage-name")
        out_container_url = f"https://{storage_name}.blob.core.windows.net/{dest_container_name}?{sas_token}"

        #print("sas_token=", sas_token)
        #print("out url=", out_container_url)
        return out_container_url

    def add_tasks_to_job(self, node_records):
        #print(f'Adding {self.num_nodes} tasks to job [{self.job_id}]...')

        # we always use exactly 1 task per node (xt controller)
        tasks = []
        for idx, node_record in enumerate(node_records):
            #cmd = "/bin/bash -c \"cat {}\"".format(input_file.file_path)
            node_cmd = node_record["node_cmd"]
            node_res_files = node_record["node_res_files"]
            node_output_files = node_record["node_output_files"]
            
            task_id = f"task{idx}"
            #print("add task: id=", task_id, ", cmd=", cmd)

            # this is so that we can run SUDO on our cmd line (related to bug in "conda create" that requires SUDO)
            elevated_user = self.get_elevated_user_identify()

            task_param = batch.models.TaskAddParameter(id=task_id, command_line=node_cmd, 
                resource_files=node_res_files, user_identity=elevated_user, output_files=node_output_files)

            tasks.append(task_param)

        # this statement launches the job
        self.batch_client.task.add_collection(self.job_id, tasks)

        ### bug workaround: setting "on_all_tasks_complete" below doesn't seem to work so
        ### we set it on job creation (above)

        # now that we have added all our tasks, terminate the job as soon as all tasks complete (with or without error)
        #self.job.on_all_tasks_complete = "terminatejob"
        #print("self.job.on_all_tasks_complete=", self.job.on_all_tasks_complete)

    def build_output_files(self, dest_container_name, blob_path, wildcard_names):
        '''
        For each wildcard string in wildcard_names, build an OutputFile instance that specifies:
            - the source files on the node (specified by the wildcard)
            - the blob destination in the dest_container_name 

        Return the list of OutputFiles built.
        '''
        out_container_url = self.get_outfiles_container_url(dest_container_name)
        output_files = []

        for pattern in wildcard_names:
            # CAUTION: "batchmodels" is NOT the same as batch.models
            upopts = batchmodels.OutputFileUploadOptions(upload_condition="taskCompletion")

            if utils.has_azure_wildcards(pattern):
                dest_blob_path = blob_path
            else:
                # single file names require adjust to blob_path
                dest_blob_path = blob_path + "/" + os.path.basename(pattern)

            dest = batchmodels.OutputFileBlobContainerDestination(container_url=out_container_url, path=dest_blob_path)
            dest2 = batchmodels.OutputFileDestination(container=dest)

            output_file = batchmodels.OutputFile(file_pattern=pattern, destination=dest2, upload_options=upopts)
            #print("built output_file: pattern=", pattern, ", dest_container=", out_container_url, ", blob_path=", blob_path)
            output_files.append(output_file)

        return output_files

    def print_status_text(self, task_counts, wait_steps):
        # print out status codes as we wait
        #print("task_counts=", task_counts)

        status = ""
        for _ in range(task_counts.active):
            status += "q"
        for _ in range(task_counts.running):
            status += "r"
        for _ in range(task_counts.failed):
            status += "f"
        for _ in range(task_counts.succeeded):
            status += "s"

        if len(status) == 0:
            # something went wrong
            status = "."
        elif len(status) > 1:
            # more than one task, separate each sample by a space
            status += " "

        print(status, end="")
        if wait_steps > 0 and wait_steps % 60 == 0:
            print("")
            
        sys.stdout.flush()

    def wrapup_parent_run(self, store, ws, run_name):
        '''
        wrap up a run from an azure job.  run may have spawned child runs, which also need to be cleaned up.
        '''
        records = self.wrapup_target_run(store, ws, run_name)
        child_records = [rec for rec in records if rec["event"] == "child_created"]
        child_names = [rec["data"]["child_name"] for rec in child_records]

        for child_name in child_names:
            self.wrapup_target_run(store, ws, child_name)

    def wrapup_target_run(self, store, ws, run_name):
        '''
        wrap up a run from an azure job.  run may have started, or may have completed.  
        '''
        # get some needed info from run log
        records = store.get_run_log(ws, run_name)

        # is a wrapup needed?
        end_record = [rec for rec in records if rec["event"] == "ended"]
        if not end_record:
            dd = records[0]["data"]
            exper_name = dd["exper_name"]
            job_id = dd["job_id"]
            status = "killed"
            exit_code = None
            rundir = None      # since job has not started
            log = self.config.get("general", "log")
            capture = self.config.get("general", "capture")
            after_files_list = self.config.get("general", "after-files")
            metric_rollup_dict = self.config.get("metrics", None)

            aggregate_dest = self.config.get("hp-search", "aggregate-dest")
            dest_name = exper_name if aggregate_dest == "experiment" else job_id

            store.wrapup_run(ws, run_name, aggregate_dest, dest_name, status, exit_code, 
                metric_rollup_dict, rundir, after_files_list, log, capture)

        return records

    def kill_job_node(self, store, job_id, node_index, full_run_names):
        pool_id = None
        node_id = None
        task_killed = False

        if not self.batch_client:
            self.create_batch_client()

        # terminate the TASK
        #print("killing: job={}, node_index={}, run_names={}".format(job_id, node_index, full_run_names))

        task = self.batch_client.task.get(job_id, "task" + str(node_index))
        #print("task.state=", task.state)

        if task.node_info:
            pool_id = task.node_info.pool_id
            node_id = task.node_info.node_id

        if task.state != "completed":
            try:
                self.batch_client.task.terminate(job_id, task.id)     
                print("azure-batch task terminated: {}.{}".format(job_id, task.id))
                task_killed = True
            except:
                pass

        # kill the NODE itself
        # TODO: we need the resource_group to make this call
        #self.batch_client.node.delete(resource_group, node_id)

        # wrap-up each run (logging, capture)
        kill_results = []

        if task_killed and full_run_names:
            for full_run_name in full_run_names:    
                ws, run_name = full_run_name.split("/")
                # now, wrapup all runs for the specified azure batch box

                self.wrapup_parent_run(store, ws, run_name)
                kr = {"workspace": ws, "run_name": run_name, "killed": True, "status": "killed"}
                #print("kr=", kr)
                kill_results.append(kr)
 
        #print("kill_results=", kill_results)
        return kill_results, pool_id

    def kill_job(self, store, job_id, runs_by_box=None):
        kill_results_by_box = {}
        pool_id = None

        if runs_by_box:
            for node_index, box_name in enumerate(runs_by_box.keys()):
                run_names = runs_by_box[box_name]

                # kill the NODE and associated runs
                kill_results_by_box[box_name], pool_id = self.kill_job_node(store, job_id, node_index, run_names) 

        # terminate the JOB
        try:
            self.batch_client.job.terminate(job_id, terminate_reason="killed by user")
            #print("job terminated: " + str(job_id))
        except BaseException as ex:
            #raise ex
            utils.user_error("job not running: " + job_id)

        # delete the POOL
        if pool_id:
            try:
                self.batch_client.pool.delete(pool_id)
                print("pool deleted: " + str(pool_id))
            except:
                pass

        return kill_results_by_box

    def get_job_status(self, job_id):
        if not job_id:
            job_id = self.job_id

        print("get_job_status (azure): job_id=", job_id)

        if not self.batch_client:
            self.create_batch_client()
        
        try:
            status = "running"
            task_counts = self.batch_client.job.get_task_counts(job_id)
            if task_counts.active:
                # if any tasks are waiting for a node, consider the job status as allocating
                status = "allocating"    
            elif task_counts.running == 0:
                status = "completed"
        except:
            # job deleted/unknown/corrput
            status = "unknown"
        
        return status

    def attach_task_to_console(self, job_id, run_name):
        self.job_id = job_id

        self.create_batch_client()

        all_tasks_complete = False
        start = datetime.datetime.now()
        detach_requested = False
        print()

        with KeyPressChecker() as checker:
            # wait until job starts
            while True:   
                
                # get a dict of the stats for each task
                task_counts = self.batch_client.job.get_task_counts(self.job_id)

                elapsed = utils.elapsed_time(start)
                print(f"waiting for queued job to start... (elapsed time: {elapsed})", end="\r")

                all_tasks_complete = task_counts.running or task_counts.failed or task_counts.succeeded
                if all_tasks_complete:
                    break

                # check every .5 secs for keypress to be more responsive (but every 1 sec for task counts)
                ch = checker.getch_nowait()
                if ch == 27:
                    detach_requested = True
                    break
                time.sleep(.5)

                ch = checker.getch_nowait()
                if ch == 27:
                    detach_requested = True
                    break
                time.sleep(.5)

        print()     # end the status line of "..."
        sys.stdout.flush()

        if detach_requested:
            print("\n--> experiment detached from console.  to reattach, run:")
            print("\txt attach " + run_name)
        else:
            #----- stream output to console ----
            self.print_task_output(self.job_id, 0)

    def print_task_output(self, job_id, task_index):

        # get task_id
        tasks = self.batch_client.task.list(self.job_id)
        print("task.list len=", len(tasks))
        
        task = next(iter(tasks), None)
        if not task:
            print("error - job has no tasks")
        else:
            task_info = self.batch_client.task.get(self.job_id, task.id)
            node_info = task_info.node_info

            if node_info:
                # node has been allocated and not yet released
                stream = self.batch_client.file.get_from_task(self.job_id, task.id, "stdout.txt")

                while True:
                    for data in stream:
                        text = data.decode("utf-8")
                        print(text)

                    task_counts = self.batch_client.job.get_task_counts(self.job_id)
                    if task_counts.running == 0:
                        print("<task terminated>")
                        break

                    time.sleep(1)

                #print(f"\nTask: {task.id}, Node: {node_id}, Standard output:")
                #print(file_textt)
            else:
                print("error - task has no node")

    def print_output_for_tasks(self):
        """Prints the stdout.txt file for each task in the job.
        """
        print('Printing task output...')

        tasks = self.batch_client.task.list(self.job_id)

        for task in tasks:
            print(f"getting output for job={self.job_id}, task={task.id}")
            
            task_info = self.batch_client.task.get(self.job_id, task.id)
            node_info = task_info.node_info

            if node_info:
                node_id = node_info.node_id
                stream = self.batch_client.file.get_from_task(self.job_id, task.id, "stdout.txt")
                file_text = self._stream_to_text(stream)

                print(f"\nTask: {task.id}, Node: {node_id}, Standard output:")
                print(file_text)

    def _stream_to_text(self, stream, encoding='utf-8'):
        output = io.BytesIO()

        try:
            for data in stream:
                output.write(data)
            return output.getvalue().decode(encoding)
        finally:
            output.close()

        raise RuntimeError('could not read task data from stream')

    def convert_blobs_to_resource_files(self, container_name, blob_names, file_names, writable=False, expire_hours=24):
        if writable:
            permission = azureblob.BlobPermissions.WRITE
        else:
            permission = azureblob.BlobPermissions.READ

        resource_files = []

        #for blob_name, file_name in zip(blob_names, file_names):
        for i, blob_name in enumerate(blob_names):
            # create a security token to allow anonymous access to blob
            expire_date = expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=expire_hours)

            sas_token = self.blob_client.generate_blob_shared_access_signature(container_name,
                blob_name, permission=permission, expiry=expire_date)

            # convert SAS to URL
            sas_url = self.blob_client.make_blob_url(container_name, blob_name, sas_token=sas_token)

            # support OPTIONAL file_names
            file_name = file_names[i] if file_names else "./"

            # finally, create the ResourceFile
            resource_file = batchmodels.ResourceFile(http_url=sas_url, file_path=file_name)
            resource_files.append(resource_file)

        return resource_files

    # def download_blobs_to_files(self, container_name, blob_path, blob_names, dest_path):
    #     file_names = []
    #     for blob_name in blob_names:

    #         if blob_name.startswith(blob_path):
    #             # remove blob_path/ from start of blob_name
    #             base_blob_name = blob_name[len(blob_path)+1:]
    #         else:
    #             base_blob_name = blob_name
                
    #         fn = dest_path + "/" + base_blob_name
    #         self.blob_client.get_blob_to_path(container_name, blob_name, fn)
    #         file_names.append(fn)

    #     return file_names

    def upload_files_to_blobs(self, container_name, blob_path, files):
        # create container if needed
        self.blob_client.create_container(container_name, fail_on_exist=False)
        #print("result from create_container=", result)

        # upload input files from local machine to Azure Store as blobs
        #print(f'Uploading file {file_path} to container [{container_name}]...')

        blob_names = []
        for fn in files:
            blob_dest = os.path.basename(fn)
            if blob_path:
                blob_dest = blob_path + "/" + blob_dest
            self.blob_client.create_blob_from_path(container_name, blob_dest, fn)
            blob_names.append(blob_dest)

        return blob_names

    def close_resources(self, batch_client):

        if self.pool_id:
            print("deleting pool...")
            batch_client.pool.delete(self.pool_id)
            self.pool_id = None

        if self.job_id:
            print("deleting job...")
            batch_client.job.delete(self.job_id)
            self.job_id = None
