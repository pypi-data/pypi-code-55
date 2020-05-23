 # py: common functions shared among XT modules

import os
import sys
import json
import time
import arrow
import shutil
import socket 
import fnmatch
import datetime
import subprocess
import tempfile
import traceback

# constants
BUILD = "v.0.0.96 build Aug-20-2019"

OVERRIDES_FN = "./xt_config_overrides.toml"

# workspace directory and files
WORKSPACE_DIR = "__ws__"
RUNS_DIR = "runs"
EXPERIMENTS_DIR = "experiments"
HOLDER_FILE = "__make_dir__"
WORKSPACE_LOG = "workspace.log"
WORKSPACE_NEXT = "next_run_number.control"
SHARED_FILES = "shared_files"

# run LOG files
ALL_RUNS_CACHE_FN = "allruns/$aggregator/all_runs.json"   
RUN_LOG = "run.log"                 # single run (stored in run dir)
ALL_RUNS_FN = "all_runs.jsonl"      # job/experiment set of runs

# run SUMMARY files
RUN_SUMMARY_CACHE_FN = "summaries/$ws/summary.json"
RUN_SUMMARY_LOG = "run_summary.log"      # single run (stored in run dir)
WORKSPACE_SUMMARY = "run_summary.log"    # all runs (stored in workspace)

# run names by JOB/EXPERIMENT
AGGREGATED_RUN_NAMES_FN = "aggregated_run_names.txt"     # runs that have ENDED

INFO_CONTAINER = "xt-store-info"
INFO_DIR = "__info__"
JOBS_NEXT = "next_job_number.control"
JOBS_DIR = "jobs"
JOB_INFO_FN = "job_info.json"
JOB_LOG = "job.log"               # info about a job

# run names
RUN_STDOUT = "console.txt"
RUN_STDERR = "console.txt"

# hyperparameter config file
HP_CONFIG_DIR = "hp-confg-dir"
HP_CONFIG_FN = "hp_config.txt" 
HP_SWEEP_LIST_FN = "sweeps-list.json"

BOX_WD = "~/xt_run"
CONTROLLER_PORT = 18861
AZURE_BATCH_BASE_CONTROLLER_PORT = 7500  

# files that capture controller output
CONTROLLER_SCRIPT_LOG = "~/.xt/controller_script.log"        # output of batch/script file that launches controller
CONTROLLER_RUN_LOG = "~/.xt/controller_run.log"              # output of cmd that runs controller
CONTROLLER_INNER_LOG = "~/.xt/controller_inner.log"          # stdout capture from within controller code

# script/batch files used to launch the controller
CONTROLLER_SHELL = "~/.xt/run_controller.sh"
CONTROLLER_BATCH = "~/.xt/run_controller.bat"
        
APP_EXIT_MSG = "@__app_exit__:"
TEMP_SCRIPT = "$TEMP/xt_script"

LOCAL_KEYPAIR_PRIVATE = "~/.ssh/xt_id_rsa"
LOCAL_KEYPAIR_PUBLIC = "~/.ssh/xt_id_rsa.pub"

FN_MULTI_RUN = "xtc_multi_run_context.json"

# utils internal variables
xt_started = None
xt_last_time = None
timing_enabled = False
diagnostics = False

def set_timing_data(started, enabled):
    global xt_started, timing_enabled, xt_last_time
    xt_started = started
    xt_last_time = started
    timing_enabled = enabled

def timing(msg):
    global xt_started, timing_enabled, xt_last_time
    if timing_enabled:
        elapsed = time.time() - xt_started
        delta = time.time() - xt_last_time
        xt_last_time = time.time()
        print("[{:.2f}, +{:.2f}]: {}".format(elapsed, delta, msg))

def dict_default(dd, key, default_value=None):
    return dd[key] if key in dd else default_value

def diag(msg):
    if diagnostics:
        print(msg)

def feedback(msg, is_first=False, is_final=False):
    post = "" if is_final else ", "
    end = "\n" if is_final else ""

    print(msg + post, end=end)
    sys.stdout.flush()

def is_windows():   
    return os.name == "nt"

def get_conda_env():
    conda_env = os.getenv("CONDA_DEFAULT_ENV")
    #print("conda_env=", conda_env)
    return conda_env

def exception_msg(ex):
    parts = str(ex).split("\n")
    return parts[0]

def internal_error(msg):
    raise Exception("Internal XT Error: " + msg)

def user_error(msg):
    #print("throwing exception...")
    raise Exception("Error: " + msg)

def user_exit(msg):
    raise Exception(msg)

def report_exception(ex, operation=None):
    #print("Error - " + exception_msg(ex))
    raise ex

def dict_to_object(prop_dict):
    class BagObject:
        def __init__(self, **prop_dict):
            self.__dict__.update(prop_dict)

    return BagObject(**prop_dict)

def get_num_from_job_id(job_id):
    # job341
    return job_id[3:]

def get_hostname():
    return socket.gethostname().lower()

def has_azure_wildcards(name):
    has_wild = "*" in name
    return has_wild

def is_azure_batch_box(box_name):
    return box_name == "azure-batch" or box_name.startswith("job")


def is_localhost(box_name, box_addr=None):
    is_local = False

    if box_name:
        box_name = box_name.lower()
        is_local = (box_name in ["local", "localhost"]) or (box_name == get_hostname())

    # for now, we rely on box_name = HOSTNAME for localhost machines

    if not is_local and box_addr:
        if box_addr in ["local", "localhost"]:
            is_local = True
        else:
            if "@" in box_addr:
                box_addr = box_addr.split("@")[1]
            is_local = (box_addr == get_ip_address())

    return is_local

def full_run_name(store_type, ws, run_name):
    #return "xt-{}://{}/{}".format(store_type, ws, run_name)
    if "/" in run_name:
        full_name = run_name
    else:
        full_name = "{}/{}".format(ws, run_name)
    return full_name

def parse_run_name(default_ws, run_name):
    if "/" in run_name:
        parts = run_name.split("/")
        if len(parts) != 2:
            user_error("invalid format for run name: " + run_name)
        ws, run_name = parts
    else:
        ws = default_ws
    return ws, run_name

def is_simple_run_name(text):
    return isinstance(text, str) and text.startswith("run") and len(text) > 3 and text[3].isdigit()

def is_well_formed_run_name(text):
    well_formed = True
    if not "*" in text:
        if "/" in text:
            parts = text.split("/")
            if len(parts) != 2:
                well_formed = False
            elif not is_simple_run_name(parts[1]):
                well_formed = False
        elif not is_simple_run_name(text):
            well_formed = False
    return well_formed

def validate_run_name(store, ws, run_name, error_if_invalid=True):
    if "/" in run_name:
        parts = run_name.split("/")
        if len(parts) != 2:
            user_error("invalid format for run name: " + run_name)
        ws, run_name = parts

    run_name = run_name.lower()
    if not "*" in run_name:
        if not store.does_run_exist(ws, run_name):
            if error_if_invalid:
                user_error("run '{}' does not exist in workspace '{}'".format(run_name, ws))
            else:
                return None, None, None
    return ws, run_name, ws + "/" + run_name

def old_get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip  

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def make_text_display_safe(text):
    tbytes = text.encode(sys.stdout.encoding, errors='replace')
    text = tbytes.decode("utf-8", "replace")
    return text

def load_json_records(text):
    # each line is a JSON text record, with a newline at the end
    json_text = "[" + text.replace("\n", ",")[0:-1] + "]"
    records = json.loads(json_text)
    return records

def format_store(store):
    return f"{store}://"  

def format_workspace(store, ws_name):
    return "store={}, workspace={}".format(store.upper(), ws_name.upper())

def format_workspace_exper_run(store_type, ws_name, exper_name, run_name):
    #return f"{store_type}://{ws_name}/{exper_name}/{run_name}"
    return f"{ws_name}/{run_name}"

def get_xthome_dir():
    return get_home_dir() + "/.xt"

def get_home_dir():
    if is_windows():
        # running on windows
        home_dir = os.getenv('USERPROFILE') 
        home_dir = home_dir.replace("\\", "/")
    else:
        home_dir = os.getenv('HOME') 
    return home_dir 

def get_config_fn():
    return get_xthome_dir() + "/xt_config.toml"

def get_dev_config_fn():
    return get_xthome_dir() + "/xt_dev_config.toml"

def zap_file(fn):
    if os.path.exists(fn):
        os.remove(fn)

def filter_out_verbose_lines(output):
    # filter out the "debug1:" messages produced by the verbose option
    lines = output.split("\n")
    filtered_lines = []

    for line in lines:
        if line.startswith("debug1:"):
            continue
        if line.startswith("OpenSSH_for"):
            continue
        if line.startswith("Authenticated to"):
            continue
        if line.startswith("Transferred:"):
            continue
        if line.startswith("Bytes per second:"):
            continue
        filtered_lines.append(line)

    output = "\n".join(filtered_lines)
    return output

def sync_run(cmd_parts, capture_output=True, shell=False, report_error=False):
    ''' this does a synchronous run of the specified cmd/app and returns the app's exitcode. It runs
    in the current working directory, but target app MUST be a fully qualified path. '''
    universal_newlines = False

    if capture_output:
        process = subprocess.run(cmd_parts, cwd=".", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
            universal_newlines=universal_newlines, shell=shell)

        output = process.stdout

        if not universal_newlines:
            # since universal_newlines=False, we need to map bytes to str
            output = output.decode("utf-8", errors='backslashreplace').replace('\r', '')

        output = filter_out_verbose_lines(output)
    else:
        process = subprocess.run(cmd_parts, cwd=".", shell=shell)
        output = None

    exit_code = process.returncode

    if report_error and exit_code:
        print(output)
        raise Exception("sync run failed, exit code=" + str(exit_code))

    return exit_code, output

def sync_run_ssh(caller, box_addr, box_cmd, report_error=True, capture_output=True):
    '''
    This can be used to execute a cmd on the remote box, provided that an XT key
    has previously been sent to the box with the 'xt keysend' command.

    Note:
        - we use the "-i <file>" option to send public half of keypair (avoid entering password)
        - we use the "-v" (verbose) option to avoid a "quick edit" mode hanging issue (avoid ENTER key pressing)
    '''

    verbose = "-v " if capture_output else ""
    ssh_cmd = "ssh " + verbose + "-i ~/.ssh/xt_id_rsa {} {}".format(box_addr, box_cmd)
    diag("  running SSH: " + str(ssh_cmd))
    exit_code, output = sync_run(ssh_cmd, report_error=report_error, capture_output=capture_output)

    diag("  <script completed OK>")
    return exit_code, output

'''
The following 2 functions start an asynch console app using 1 of the available "console_type" values:
    - hidden, visible, integrated (on a WINDOWS machine)
    - hidden, integrated (on a LINUX machine)
    
The "hidden" and "visible" values imply a detached console whose process life is not affected by 
the parent process dying.

Tested on WINDOWS and LINUX, 4/15/2019, rfernand.  Machines used: "agent1" home machine (Windows 10)
and Azure VM "vm15" (Ubuntu 16.04.5 LTS).

LESSONS LEARNED in developing this code:
    - the target app name MUST be a FULLY QUALIFIED path name.
    - the target app name MUST have the "~/..." part of the path expanded into true path
    - sometimes the error "No such file or directory..." means it is try to interpret the entire cmd line as a filename
    - if using creationflags=DETACHED, you must redirect STDOUT, STDERR
    - when capturing stdout, we don't have to hold the file open (cool!)
    - if running a batch file or shell script, the stdout will NOT include the child processes.
    - the "startupinfo" information seeemed to be ignored by popen.
    - lack of good error messages/mechanisms/documentation made this process somewhat challenging
'''

def start_async_run_detached(cmd, working_dir, fn_stdout, visible=False):
    DETACHED_PROCESS = 0x00000008    # if visible else 0
    CREATE_NO_WINDOW = 0x08000000
    
    if not visible and os.name == 'nt':
        # do NOT specify DETACHED_PROCESS when CREATE_WINDOW 
        cflags = CREATE_NO_WINDOW  # | DETACHED_PROCESS
    else:
        cflags = DETACHED_PROCESS

    with open(fn_stdout, 'w') as output:
        p = subprocess.Popen(cmd, cwd=working_dir, stdout=output, stderr=subprocess.STDOUT, creationflags=cflags) 
    return p

def start_async_run_integrated(cmd, working_dir):
    subprocess.Popen(cmd, cwd=working_dir)

def ensure_dir_exists(dir=None, file=None):
    if file:
        dir = os.path.dirname(file)
    
    if dir and not os.path.exists(dir):
        os.makedirs(dir)

def time_diff(time1, time2):
    return (time1 - time2).total_seconds()

def elapsed_time(start):
    diff = datetime.datetime.now() - start

    elapsed = str(diff)
    index = elapsed.find(".")
    if index > -1:
        elapsed = elapsed[0:index]

    return elapsed

def str_is_float(value):
    is_float = False
    try:
        fvalue = float(value)
        is_float = True
    except:
        pass
    return is_float

def make_numeric_if_possible(value):
    try:
        value = int(value)
    except:
        try:
            value = float(value)
        except:
            pass

    # also convert boolean values
    if isinstance(value, str):
        lower = value.lower()
        if lower == "true":
            value = True
        elif lower == "false":
            value = False

    return value

def format_elapsed_hms(elapsed, include_fraction=False):
    value = str(datetime.timedelta(seconds=float(elapsed)))
    if not include_fraction:
        index = value.find(".")
        if index > -1:
            value = value[0:index]

    return value

def enable_ansi_escape_chars_on_windows_10():
    import ctypes

    if is_windows():
        #print("***** enabling ESCAPE CHARS on screen *******")
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def open_file_with_default_app(fn):
    if is_windows():
        import os
        os.system("start " + fn)
    else:
        import webbrowser
        webbrowser.open(fn)

def expand_vars(text):
    if is_windows():
        text = text.replace("${HOME}", "${userprofile}")

    text = os.path.expandvars(text)
    return text

def make_retry_func(max_retries=8):
    #max_retries = 8     # 95 secs total retry time
    #print("received max_retries=", max_retries)

    def expo_retry(context):

        if not hasattr(context, "count"):
            context.count = 1
        else:
            context.count += 1

        status = None
        if context.response and context.response.status:
            status = context.response.status

        print("Azure Exception in XTLIB:")
        print('-'*60)
        traceback.print_exc(file=sys.stdout)
        print( '-'*60)

        if context.count > max_retries:
            backoff_time = None
            if max_retries:
                print(f"ERROR RETRY: max_retries={max_retries} exceeded")
        else:
            backoff_time = min(16, 2**context.count)
            str_exception = str(context.exception).replace('\n', '')

            if max_retries:
                print(f"\nERROR RETRY: status={status}, retry count={context.count}, backoff={backoff_time}, max_retries={max_retries}, " + 
                    f"exception={str_exception}")

        return backoff_time
    
    return expo_retry

def read_text_file(fn):
    fn = os.path.expanduser(fn)

    with open(fn, "r") as tfile:
        text = tfile.read()
    return text

def write_text_file(fn, text, newline=None):
    fn = os.path.expanduser(fn)

    with open(fn, "w", newline=newline) as tfile:
        tfile.write(text)

def scp_copy_file_to_box(caller, box_addr, fn_local, box_fn, report_error=True):
    cmd = 'scp -i {} "{}" {}:{}'.format(LOCAL_KEYPAIR_PRIVATE, fn_local, box_addr, box_fn)
    diag("  copying script to box; cmd=" + cmd)

    exit_code, output = sync_run(cmd)
    if report_error and exit_code:
        print(output)
        raise Exception("scp copy command failed")

def send_cmd_as_script_to_box(caller, box_addr, cmd_to_run, box_script_path, prep_script, linux_box=True):
    script = ""
    #print("send_cmd_as_script_to_box: box_addr=", box_addr, ", box_script_path=", box_script_path)

    if linux_box:
        # create LINUX .sh script
        script += "#!/bin/sh" + "\n"
        if prep_script:
            script += "\n".join(prep_script)
        script += "\n" + cmd_to_run + "\n"
        diag("  created Linux sh script: \n" + script)
    else:
        # create Windows .bat script
        if prep_script:
            # for detacted window support, we must prepend "@" on front of each cmd
            for ps in prep_script:
                if not ps.startswith("@"):
                    ps = "@" + ps
                script += ps + "\n"

        script += "@" + cmd_to_run + "\n"
        diag("  created Windows .bat file: \n" + script)

    # copy script to box
    if is_localhost(None, box_addr):
        # write script directly to box_script_path
        write_text_file(box_script_path, script, newline="")

        if linux_box:
            # mark it as executable
            #parts = ["chmod", "+x", box_script_path]
            parts = "chmod +x {}".format(box_script_path)
            diag("  marking linux script as executable: " + str(parts))
            sync_run(parts, shell=True, report_error=True)
            diag("  <script completed OK>")
    else:
        # write script to temp file
        fn_script = expand_vars(TEMP_SCRIPT)
        write_text_file(fn_script, script, newline="")
        diag("  script written to TMP FILE=" + str(fn_script))

        # copy from temp to box
        diag("  copying file to box: " + box_script_path)
        scp_copy_file_to_box(caller, box_addr, fn_script, box_script_path, report_error=True)
        diag("  <copy completed OK>")

        if linux_box:
            # mark it as executable
            box_cmd = "chmod +x {}".format(box_script_path)
            sync_run_ssh(caller, box_addr, box_cmd)

def input_with_default(prompt, default, dim_prompt=True):
    if is_windows:
        # WINDOWS
        import win32console
        _stdin = win32console.GetStdHandle(win32console.STD_INPUT_HANDLE)
        keys = []
        for c in default:
            evt = win32console.PyINPUT_RECORDType(win32console.KEY_EVENT)
            evt.Char = c
            evt.RepeatCount = 1
            evt.KeyDown = True
            keys.append(evt)

        _stdin.WriteConsoleInput(keys)

        if dim_prompt:
            enable_ansi_escape_chars_on_windows_10()
            gray = "\033[0;37m"
            darkgray = "\033[1;30m"
            value = input(darkgray + prompt + gray)
        else:
            value = input(prompt)

    else:
        # LINUX
        import readline
        readline.set_startup_hook(lambda: readline.insert_text(default))
        try:
            value = input(prompt)  
        finally:
            readline.set_startup_hook()

    return value

def move_cursor_up(line_count, clear_lines=True):
    # if clear_lines:
    #     # clear current line
    #     sys.stdout.write("\r\033[K") 

    for _ in range(line_count):
        sys.stdout.write("\033[F") 
        if clear_lines:
            # clear line we just moved into
            sys.stdout.write("\033[K") 

def clear_line():
    sys.stdout.write("\033[K") 

def wait_for_escape(checker, wait_time=1, check_time=.1):
    ''' 
    for this to work, it must be run inside of a
    "with KeyPressChecker() as checker:" type block
    '''

    found_escape = False
    checks = int(wait_time/check_time)  

    for check in range(checks):
        if checker.getch_nowait() == 27:
            found_escape = True
            break
        time.sleep(check_time)

    return found_escape

def print_elapsed(start, operation):
    elapsed = time.time() - start
    print("{} took: {:.2f} secs".format(operation, elapsed))

def glob(wildpath):
    ''' workaround for glob, which doesn't match
    files/directories that being with a "."
    '''
    #wildpath = os.path.abspath(wildcard)
    dirname = os.path.dirname(wildpath)
    basename = os.path.basename(wildpath)

    # set PATH and PATTERN correctly
    if os.path.isdir(wildpath):
        path = wildpath
        pattern = "*"
    else:
        # either basename is file, contains wildcard, or is part of a non-existing path
        path = dirname
        pattern = basename

    if not path:
        path = "."

    if dirname:
        dirname += "/"

    if os.path.exists(path):
        files = os.listdir(path)

        files = [dirname + name for name in files if fnmatch.fnmatch(name, pattern)]
    else:
        files = []
    return files

def records_in_sync(records, records2):
    in_sync = True

    for r1, r2 in zip(records, records2):
        t1 = arrow.get(r1["time"])
        t2 = arrow.get(r2["time"])
        delta = min((t1-t2).seconds, (t2-t1).seconds)
        #print("delta=", delta)

        if delta > .5:
            in_sync = False
            break

    #print("returning in_sync: ", in_sync)
    return in_sync

def merge_records(records, records2):   
    for r, r2 in zip(records, records2):
        #print("r2=", r2)    
        for key,value in r2.items():    
            if key != "time":
                r[key] = value

def build_metrics_sets(records):
    '''
    builds a collection of metrics sets.  A metric set is a set of metrics that have been reported together 
    in the run log.  Here 'together' means as a single log entry, or in entires 
    timestamped within a few tenths of a second.

    'records' is the set of dict records of a run log.
    '''
    # first step: put each metric into their own set (with time-stamped records)
    own_sets = {}

    for log_dict in records:
        if not log_dict:
            continue

        if not "event" in log_dict or not "data" in log_dict or log_dict["event"] != "metrics":
            continue

        dd = log_dict["data"]
        for key,value in dd.items():
            if not key in own_sets:
                own_sets[key] = []
            record = {"time": log_dict["time"], key: value}
            own_sets[key].append(record)

    # now merge metrics that were reported in sync
    merged_sets = []
    for key, own_set in own_sets.items():
        # find that merged_set that goes with this key
        merged = False
        #print("finding a merge for key=", key)

        for ms in merged_sets:
            if len(own_set) == len(ms["records"]):
                #print("checking in-sync: key={}, ms.key={}".format(key, ms["keys"][0]))

                if records_in_sync(ms["records"], own_set):
                    merge_records(ms["records"], own_set)
                    ms["keys"].append(key)
                    #print("after merge: keys=", ms["keys"])
                    merged = True
                    break

        if not merged:
            # add a new merged set
            ms = {"keys": [key], "records": own_set}
            merged_sets.append(ms)  
        
    return merged_sets

def validate_job_name(job_id):
    if job_id:
        safe_job_id = str(job_id)
        if not safe_job_id.startswith("job"):
            user_error("job id must start with 'job': " + safe_job_id)

def make_tmp_dir(prefix, fixed_name=True):
    '''create a temp directory (ensure it is empty)
    :param prefix: specifies a prefix or name to use when naming the temp dir
    :param fixed_name: when fixed_name=True, the prefix will be used to form a fixed 
     path for the directory, and the caller does NOT have to remove the directory after 
     it's usage is completed.  When fixed_name=False, the caller IS responsible for removing the directory. 
    '''
    # :param:
    if fixed_name:
        tmp_dir = os.path.expanduser("~/.xt/tmp/" + prefix)
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        os.makedirs(tmp_dir)
    else:
        tmp_dir = tempfile.mkdtemp(prefix=prefix)

    return tmp_dir

def fix_slashes(fn, force_linux=False):
    fn = os.path.expanduser(fn)
    if is_windows() and not force_linux:
        fn = fn.replace("/", "\\")
    else:
        fn = fn.replace("\\", "/")
    return fn

def strip_leading_dashes(value):
    while value.startswith("-"):
        value = value[1:]
    return value

def path_join(*argv):
    # we cannot rely on os.path.join() since it is designed for the current OS
    # we always use forward slashes which python makes work in both Linux and Windows
    path = "/".join(argv)
    return path
