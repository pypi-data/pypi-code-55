#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# psm.py: pool service manager
'''
    - this file should not reference xtlib or other non-standard libraries.
    - this is to keep deployment simple: copy & run on dest machine

    - NOTE: we currently use psutil library (non-standard) that may need 
      to be installed on some systems.  is there an alternative to this?
'''
import os
import time
import shutil
import zipfile
import datetime
import subprocess

is_windows = (os.name == "nt")
#print("is_windows:", is_windows)

PSM_QUEUE = os.path.expanduser("~/.xt/psm_queue")
PSM_LOGDIR = os.path.expanduser("~/.xt/psm_logs")
CWD = "c:/xt_controller/xt/cwd" if is_windows else  os.path.expanduser("~/.xt/cwd")

PSM = "psm.py"
CURRENT_RUNNING_ENTRY = "_current_running_entry_.txt"
FN_WRAPPER = os.path.join(CWD, "wrapped.bat" if is_windows else "wrapped.sh")
CONTROLLER_NAME_PATTERN = "xtlib.controller"
PY_RUN_CONTROLLER ="__run_controller__.py"

def get_controller_wrapped_counts():
    import psutil

    processes = psutil.process_iter()
    controller_count = 0
    wrapped_count = 0

    if is_windows:
        WRAPPED_PARTIAL = "xt\\cwd\\wrapped.bat"
    else:
        WRAPPED_PARTIAL = "xt/cwd/wrapped.sh"

    #print("  WRAPPED_PARTIAL: " + WRAPPED_PARTIAL)

    for p in processes:
        try:
            process_name = p.name().lower()
            #print("process_name=", process_name)

            if process_name.startswith("python") or "bash" in process_name:
                #print("process name: {}".format(p.name()))
                cmd_line = " ".join(p.cmdline())
                #print("  cmd_line: " + cmd_line)

                if CONTROLLER_NAME_PATTERN in cmd_line or PY_RUN_CONTROLLER in cmd_line:
                    controller_count += 1
                elif WRAPPED_PARTIAL in cmd_line:
                    wrapped_count += 1

        except BaseException as ex:
            pass
        
    return controller_count, wrapped_count

def start_async_run_detached(cmd, working_dir, fn_stdout):
    DETACHED_PROCESS = 0x00000008    # if visible else 0
    CREATE_NO_WINDOW = 0x08000000
    
    print("  starting cmd=", cmd)

    with open(fn_stdout, 'w') as output:

        if is_windows:
            cflags = CREATE_NO_WINDOW  # | DETACHED_PROCESS
            p = subprocess.Popen(cmd, cwd=working_dir, stdout=output, stderr=subprocess.STDOUT, creationflags=cflags)

        else:
            # linux
            p = subprocess.Popen(cmd, cwd=working_dir, stdout=output, stderr=subprocess.STDOUT)
    return p

def start_entry(fn_entry):
    '''
    Args:
        fn_entry: name of .zip file (w/o dir):  team.job.node.ticks.zip
    '''

    # UNZIP code from entry to CWD
    fn_zip = os.path.join(PSM_QUEUE, fn_entry)
    print("  unzipping '{}' to: {}".format(fn_zip, CWD), flush=True)

    with zipfile.ZipFile(fn_zip, 'r') as zip:
        zip.extractall(CWD)

    # DELETE .zip file from queue
    os.remove(fn_zip)

    # write "current job running" file
    fn_current = os.path.join(CWD, CURRENT_RUNNING_ENTRY)
    with open(fn_current, "wt") as outfile:
        outfile.write(fn_entry)

    now = datetime.datetime.now()
    print("{}: PSM starting entry:\n  {}".format(now, fn_entry))

    # start file
    try:
        fn_wrapper = FN_WRAPPER
        if is_windows:
            # fix slashes
            fn_wrapper = fn_wrapper.replace("/", "\\")

        if fn_wrapper.endswith(".bat"):
            cmd_parts = [fn_wrapper]
        else:
            cmd_parts = ["bash", "--login", fn_wrapper]

        fn_base_entry = os.path.splitext(fn_entry)[0]
        fn_log = os.path.join(PSM_LOGDIR, fn_base_entry + ".log")

        # run PSM on remote box
        start_async_run_detached(cmd_parts, ".", fn_log)

    except BaseException as ex:
        print("error during start of entry: ex=", ex)
        raise ex

def print_queue(msg):
    files = os.listdir(PSM_QUEUE)

    print(msg)
    for entry in files:
        print("  {}".format(entry))

def main():
    now = datetime.datetime.now()
    print("PSM starting:", now)

    # ensure PSM_QUEUE exist
    if not os.path.exists(PSM_QUEUE):
        os.makedirs(PSM_QUEUE)

    # ensure PSM_LOGDIR exist
    if not os.path.exists(PSM_LOGDIR):
        os.makedirs(PSM_LOGDIR)

    last_entry_count = 0

    while True:
        time.sleep(5)

        # list queue
        files = os.listdir(PSM_QUEUE)
        entry_count = len(files)

        # anything in queue?
        if entry_count:

            now = datetime.datetime.now()
            controller_count, wrapped_count = get_controller_wrapped_counts()
            
            if last_entry_count != entry_count:
                print("{}: found {} entries in queue (controller_count={}, wrapped_count={})".format(now, len(files), controller_count, wrapped_count))
                last_entry_count = entry_count
                print_queue("queue:")
            
            if (controller_count + wrapped_count) == 0:
                # sort job entries by ticks part of fn   (team.job.node.ticks.zip)
                files.sort( key=lambda fn: int(fn.split(".")[-2]) )

                # use oldest file (smallest tick value) to XT cwd
                fn_entry = files[0]
                start_entry(fn_entry)


if __name__ == "__main__":
    main()
