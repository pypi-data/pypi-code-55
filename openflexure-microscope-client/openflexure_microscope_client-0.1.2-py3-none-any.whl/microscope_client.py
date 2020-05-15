"""
Simple client code for the OpenFlexure Microscope in Python

Copyright 2020 Richard Bowman, released under LGPL 3.0 or later
"""

import requests
import json
import time
import io
import PIL.Image
import numpy as np
import logging
import zeroconf

class MicroscopeClient(object):
    def __init__(self, host, port=5000):
        if isinstance(host, zeroconf.ServiceInfo):
            # If we have an mDNS ServiceInfo object, try each address
            # in turn, to see if it works (sometimes you get addresses
            # that don't work, if your network config is odd).
            # TODO: figure out why we can get mDNS packets even when
            # the microscope is unreachable by that IP
            for addr in host.parsed_addresses():
                if ":" in addr:
                    self.host = f"[{addr}]"
                else:
                    self.host = addr
                self.port = host.port
                try:
                    self.get_json(self.base_uri)
                    break
                except:
                    logging.info(f"Couldn't connect to {addr}, we'll try another address if possible.")
        else:
            self.host = host
            self.port = port
        logging.info(f"Connecting to microscope {self.host}:{self.port}")
        self.populate_extensions()

    extensions = None
        
    @property
    def base_uri(self):
        return f"http://{self.host}:{self.port}/api/v2"

    def get_json(self, path):
        """Perform an HTTP GET request and return the JSON response"""
        if not path.startswith("http"):
            path = self.base_uri + path
        r = requests.get(path)
        r.raise_for_status()
        return r.json()

    def post_json(self, path, payload={}, wait_on_task="auto"):
        """Make an HTTP POST request and return the JSON response"""
        if not path.startswith("http"):
            path = self.base_uri + path
        r = requests.post(path, json=payload)
        r.raise_for_status()
        r = r.json()
        if wait_on_task == "auto":
            wait_on_task = is_a_task(r)
        if wait_on_task:
            return poll_task(r)
        else:
            return r

    def populate_extensions(self):
        """Get the list of extensions and store it in self.extensions"""
        extension_list = self.get_json("/extensions/")
        self.extensions = {v["title"]: MicroscopeExtension(v) for v in extension_list}

    @property
    def position(self):
        """Return the position of the stage as a dictionary"""
        response = self.get_json("/instrument/state/stage/position")
        return response

    def get_position_array(self):
        """Return the position of the stage, as an array"""
        pos = self.position
        return np.array([pos[k] for k in "xyz"])

    def move(self, position, absolute=True):
        """Move the stage to a given position.

        WARNING! If you specify zeros, the stage might move a long way, as
        the default is absolute moves.  Position should be a dictionary
        with keys called "x", "y", and "z", although we will (for now) also
        accept an iterable of three numbers.
        """
        try:
            pos = {k: int(position[k]) for k in ["x", "y", "z"]}
        except:
            pos = {k: int(position[i]) for i, k in enumerate(["x", "y", "z"][:len(position)])}
        pos['absolute'] = absolute
        response = self.post_json("/actions/stage/move", pos)
        return response

    def move_rel(self, position):
        """Move the stage by a given amount.  Zero should not move.
        
        This function calls ``move`` with ``absolute=False``
        """
        self.move(position, absolute=False)
        
    def query_background_task(self, task):
        """Request the status of a background task"""
        r = requests.get(task['links']['self']['href'])
        r.raise_for_status()
        return r.json()

    def capture_image(self, ):
        """Capture an image and return it as a PIL image object"""
        payload = {
            "use_video_port": True,
            "bayer": False,
        }
        r = requests.post(self.base_uri + "/actions/camera/ram-capture", json=payload)
        r.raise_for_status()
        image = PIL.Image.open(io.BytesIO(r.content))
        return image

    def grab_image(self):
        """Grab an image from the stream and return as a PIL image object"""
        r = requests.get(self.base_uri + "/streams/snapshot")
        r.raise_for_status()
        image = PIL.Image.open(io.BytesIO(r.content))
        return image

    def grab_image_array(self, ):
        """Grab an image and return it as a numpy ndarray"""
        return np.array(self.grab_image())

    def calibrate_xy(self):
        """Move the stage in X and Y to calibrate stage movements vs camera coordinates
        
        NB this takes around 2 minutes to complete with a 40x objective.  Lower magnification
        may work less well.
        """
        return self.extensions["org.openflexure.camera_stage_mapping"]["calibrate_xy"].post_json()

    def autofocus(self):
        """Move the stage up and down, and pick the sharpest position."""
        return self.extensions["org.openflexure.autofocus"]["fast_autofocus"].post_json()

class MicroscopeExtension():
    """A class that represents a microscope extension"""
    def __init__(self, extension_dict):
        self.extension_dict = extension_dict

    @property
    def links(self):
        return self.extension_dict["links"]
        
    def __getitem__(self, attr):
        """Dictionary-style syntax to get the links"""
        if attr not in self.links:
            raise KeyError(f"This extension does not have a link called {attr}.")
        link = self.links[attr]
        return RequestableURI(**link)

class RequestableURI():
    def __init__(self, href, description=None, methods=None):
        """A class representing an endpoint, making it easy to make requests to said endpoint."""
        self.href = href
        self.description = description or ""
        self.methods = methods or ['GET','POST',] #TODO: what's the sensible default?

    def get_json(self):
        """Perform an HTTP GET request and return the JSON response"""
        if "GET" not in self.methods:
            raise KeyError("This URI does not support GET requests")
        r = requests.get(self.href)
        r.raise_for_status()
        return r.json()

    def post_json(self, payload=None, wait_on_task="auto"):
        """Make an HTTP POST request and return the JSON response"""
        if "POST" not in self.methods:
            raise KeyError("This URI does not support POST requests")
        r = requests.post(self.href, json=payload or {})
        r.raise_for_status()
        r = r.json()
        if wait_on_task == "auto":
            wait_on_task = is_a_task(r)
        if wait_on_task:
            return poll_task(r)
        else:
            return r

def task_href(t):
    """Extract the endpoint address from a task dictionary"""
    return t["links"]["self"]["href"]

def is_a_task(t):
    """Return true if a parsed JSON return value represents a task"""
    try:
        return "/api/v2/tasks/" in task_href(t)
    except:
        return False

def poll_task(task):
    """Poll a task until it finishes, and return the return value"""
    assert is_a_task(task), ("poll_task must be called with a "
                "parsed JSON representation of a task")
    log_n = 0
    while task["status"] in ["running", "idle"]:
        r = requests.get(task_href(task))
        r.raise_for_status()
        task = r.json()
        while len(task["log"]) > log_n:
            d = task["log"][log_n]
            logging.log(d["levelno"], d["message"])
            log_n += 1
    try:
        return task["return"]
    except:
        logging.warning("Task endpoint was missing a return value.")

def find_mdns_services(type, timeout=10, n_services=9999):
    """Look for mdns services matching `type`.

    We will stop either after `timeout` seconds, or after
    `n_services` services have been found.
    """
    zc = zeroconf.Zeroconf()
    class Listener():
        def __init__(self):
            self.services_discovered = []

        def add_service(self, zeroconf, type, name):
            info = zeroconf.get_service_info(type, name)
            self.services_discovered.append(info)
    listener = Listener()
    browser = zeroconf.ServiceBrowser(zc, type, listener)
    stop_time = time.time() + timeout
    while len(listener.services_discovered) < n_services \
        and time.time() < stop_time:
        time.sleep(0.1)
    zc.close()
    return listener.services_discovered

def find_microscopes(timeout=10, n_microscopes=99999):
    """Look for microscopes on the network.

    We will wait for responses, either for `timeout` seconds, or 
    until `n_microscopes` have been found.
    """
    return find_mdns_services(
        "_openflexure._tcp.local.", timeout, n_microscopes)

def find_first_microscope(timeout=10):
    """Returnt the first microscope we can find on the network"""
    microscopes = find_microscopes(timeout, 1)
    if len(microscopes) == 0:
        raise Exception("There are no microscopes advertised on the local network")
    return MicroscopeClient(microscopes[0])