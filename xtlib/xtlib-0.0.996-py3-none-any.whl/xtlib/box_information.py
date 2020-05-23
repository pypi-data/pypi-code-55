# box_information.py: returns info about the specified box_name
from . import utils

class BoxInfo():
    def __init__(self, config, box_name):
        self.config = config
        self.box_name = box_name

        self._set_box_info(box_name)

    def _set_box_info(self, box_name):
        if utils.is_azure_batch_box(box_name):
            # TODO: get os and class from TOML
            self.box_os = "linux"
            self.address = None
            self.box_class = "dsvm"   # use job->pool->azure_image
            self.max_runs = 1
        else:
            if box_name in self.config.get("boxes"):
                box_info = self.config.get("boxes", box_name, default_value={})
            else:
                box_info = {"max-runs": 1}
                if utils.is_localhost(box_name):
                    box_info["address"] = "localhost"
                    box_info["box-class"] = "windows" if utils.is_windows() else "linux"

            if not "address" in box_info:
                raise Exception("address property not defined for boxes[{}] in config file".format(box_name))

            # for key, value in defaults_dict.items():
            #     if not key in box_info:
            #         box_info[key] = value

            box_info["name"] = box_name

            box_addr = get_box_addr(self.config, box_name)
            if utils.is_localhost(box_name, box_addr):
                box_info["os"] = "windows" if utils.is_windows() else "linux"

            #print("box_name=", box_name, ", box_info=", box_info)

            self.box_os = box_info["os"]
            self.address = box_info["address"]
            self.box_class = box_info["box-class"]
            self.max_runs = box_info["max-runs"] if "max-runs" in box_info else 1

        self.shell_launch_prefix = self.config.get("box-class", self.box_class, "shell-launch-prefix", 
            suppress_warning=True)

    def get_box_os(self, box_name):
        #print("box_name=", box_name)
        if utils.is_azure_batch_box(box_name):
            box_os = "linux"
        elif utils.is_localhost(box_name):
            box_os = "windows" if utils.is_windows() else "linux"
        else:
            box_info = self.config.get("boxes", box_name, default_value={})
            box_os = box_info["os"] if "os" in box_info else "linux"     # default to linux
        return box_os

    def get_box_class(self, box_name):
        if utils.is_azure_batch_box(box_name):
            box_class = self.config.get("azure", "azure-image")
        elif box_name in self.config.get("boxes"):
            box_info = self.config.get("boxes", box_name, default_value={})
            box_class = box_info.box_class
        elif utils.is_localhost(box_name):
            box_class = "windows" if utils.is_windows() else "linux"
        else:
            utils.user_error("missing entry in [boxes] of xt config file for box={}".format(box_name))
        return box_class

def get_box_addr(config, box_name):
    #print("get_box_addr: box_name=", box_name)
    if utils.is_azure_batch_box(box_name):
        box_addr = None
    elif utils.is_localhost(box_name, None):
        box_addr = "localhost" 
        #print("localhost box_addr=", box_addr)
    else:
        box_addr = config.get("boxes", box_name, dict_key="address", default_value=box_name, 
            prop_error="box not defined in config file: " + box_name)
        #print("box_addr=", box_addr)

        if not "." in box_addr and box_addr != "localhost":
            raise Exception("box option must specify a machine by its IP address: " + str(box_addr))

    return box_addr

def get_box_list(core, job_id=None, explicit_boxes_only=False):
    boxes = None       
    pool_info = {}
    is_azure_pool = False
    is_azure_box = False

    # handle POOL case
    if explicit_boxes_only:
        pool = core.get_explicit_option("pool")
    else:
        pool = core.config.get("core", "pool")

    if pool:
        pool_info = get_pool_info(core, pool)
        is_azure_pool = (utils.dict_default(pool_info, "service") == "azure-batch")
        #print("pool_info=", pool_info, ", is_azure_pool=", is_azure_pool)

        if is_azure_pool:
            num_boxes = pool_info["nodes"] + pool_info["low-pri"]
            if num_boxes == 0:
                utils.user_error("no nodes or low-pri specified for azure batch pool")

            boxes = build_azure_box_names(job_id, num_boxes)
        else:
            boxes = core.config.get("pools", pool, prop_error="pool not defined in config file: " + pool)

        if not boxes:
            utils.user_error("could not find an entry for this name in the 'boxes' section of your config file: {}".format(pool))
    else:
        #print("self.box=", self.box)
        # pool not specified - handle SINGLE BOX case
        if explicit_boxes_only:
            box = core.get_explicit_option("box")
        else:
            box = core.config.get("core", "box")
            #print("pool from box=", box)

        if box:
            # lowercase all box names so they match the xt_config file
            box = box.lower()

        is_azure_box = utils.is_azure_batch_box(box) if box else False

        if box == "local":
            boxes = [utils.get_hostname()]
        elif box:
            boxes = [box]   

    #print("boxes=", boxes)

    if boxes:
        if isinstance(boxes, list):
            pass
        else:
            utils.user_error("a box must be defined as a single box entry or a pool (list of box names): {}".format(pool))

    return boxes, pool_info, is_azure_pool, is_azure_box

def get_pool_info(core, pool_name):
    if pool_name == "azure-batch":
        vm_size = core.config.get("azure", "vm-size")
        vm_image = core.config.get("azure", "azure-image")
        num_nodes = core.config.get("azure", "nodes")
        num_low_pri = core.config.get("azure", "low-pri")

        pool_info = {"service": "azure-batch", "vm-size": vm_size, "vm-image": vm_image, "nodes": num_nodes, 
            "low-pri": num_low_pri}
    else:
        pool_info = core.config.get("pools", pool_name, prop_error="pool '{}' not defined in config file".format(pool_name))

        if isinstance(pool_info, list):
            pool_info = {"boxes": pool_info}
        elif "service" in pool_info and pool_info["service"] == "azure-batch":

            # allow explicit option overriding of properties
            vm_size = core.get_explicit_option("vm-size")
            if vm_size:
                pool_info["vm-size"] = vm_size

            vm_image = core.get_explicit_option("vm-image")
            if vm_image:
                pool_info["vm-image"] = vm_image

            num_nodes = core.get_explicit_option("nodes")
            if num_nodes:
                pool_info["nodes"] = num_nodes

            num_low_pri = core.get_explicit_option("low-pri")
            if num_low_pri:
                pool_info["low-pri"] = num_low_pri

    pool_info["name"] = pool_name
    return pool_info

def build_azure_box_names(job_id, num_boxes):
    boxes = []

    # allow for early calls (before job has been created)
    if not job_id:
        job_id = ""

    for i in range(num_boxes):
        boxes.append(job_id + "-box" + str(i))

    return boxes

def get_service_params(config, job_id, box_name, node_index):
    if box_name == "azure-batch":
        box_name = job_id + "-box" + str(node_index) 
        pool = "azure-batch"
    else:
        pool = config.get("core", "pool")

    return box_name, pool

