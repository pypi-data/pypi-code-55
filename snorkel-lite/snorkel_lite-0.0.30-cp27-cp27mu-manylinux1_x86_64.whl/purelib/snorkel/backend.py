import os
import subprocess
import shlex
import json

SYBIL_BIN="sybil"

from collections import defaultdict

def run_query_command(cmd_args):
    init_cmd_args = ["sybil", "query", "-json"]
    init_cmd_args.extend(cmd_args)


    ret = run_command(init_cmd_args)

    return json.loads(ret)

def run_command(cmd_args):
    print "RUNNING COMMAND", cmd_args
    output = subprocess.check_output(cmd_args)

    return output


# time translation command is:
# `date -d "<str>" +%s`
def time_to_seconds(timestr):
    cmd_args = ["date", "-d", timestr, "+%s"]
    try:
        output = subprocess.check_output(cmd_args)
    except:
        raise Exception("Unknown time string: ", timestr)
    return int(output)

def time_delta_to_seconds(timedelta):
    now = time_to_seconds("now")
    then = time_to_seconds(timedelta)

    return now - then



class Backend(object):
    pass

FIELD_SEPARATOR=","
FILTER_SEPARATOR=":"


if __name__ == "__main__":
    print time_to_seconds('-1 week')
    print time_delta_to_seconds('-1 week')
