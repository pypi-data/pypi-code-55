import pkg_resources
try:
    version = pkg_resources.require("sequana_multitax")[0].version
except:
    version = ">=0.8.0"

