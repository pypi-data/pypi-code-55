# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

__config__ = pulumi.Config('rke')

debug = __config__.get('debug') or (utilities.get_env_bool('RKE_DEBUG') or False)

log_file = __config__.get('logFile') or (utilities.get_env('RKE_LOG_FILE') or '')

