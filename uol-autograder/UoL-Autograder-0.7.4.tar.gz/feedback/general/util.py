import inspect, os, sys
import json
import datetime
import time
from collections.abc import Mapping
from collections import namedtuple
from pathlib import Path
from tempfile import TemporaryFile
import subprocess
import threading
import psutil
from . import constants

pwd_imported = True
try:
    import pwd
except ModuleNotFoundError:
    pwd_imported = False

class Lookup:
    def __init__(self, lookup_dir):
        for name, value in inspect.getmembers(self):
            if "__" not in name and name.startswith("_") and not os.path.isabs(value):
                setattr(self, name.lstrip("_"), Path(lookup_dir, value))

decoder = lambda x: str(x.decode('UTF-8'))
dumb_decoder = lambda x: str(x).lstrip("b'", "").rstrip("'")

def setup_demotion(cwd, env):
    default_func = lambda: None

    try:
        pw_record = pwd.getpwnam(constants.RUNNER_USER)
    except KeyError:
        return env, default_func

    user_name = pw_record.pw_name
    user_home_dir = pw_record.pw_dir
    
    env['HOME']  = user_home_dir
    env['LOGNAME']  = user_name
    env['USER']  = user_name
    env['PWD']  = cwd

    subprocess.call([f"chown {constants.RUNNER_USER}: {cwd}"], shell=True)
    
    user_uid = pw_record.pw_uid
    user_gid = pw_record.pw_gid
    def demote():
        os.setgid(user_gid)
        os.setuid(user_uid)

    return env, demote

class ProcessOutOfMemoryError(Exception):
    def __init__(self):
        super().__init__("Total allowed memory usage exceeded by process")

class ProcessChildLimitHitError(Exception):
    def __init__(self):
        super().__init__("Total allowed number of child processes exceeded by process")

class ProcessWatch(threading.Thread):
    def __init__(self, proc, memory_limit=-1, child_limit=-1, polling=0.05):
        threading.Thread.__init__(self)
        self._proc = proc
        self._memory_limit = memory_limit
        self._child_limit = child_limit
        self._polling = polling
        self._pproc = psutil.Process(self._proc.pid)
        self.exception = None
    
    def run(self):
        while self._pproc.is_running():
            try:
                children = self._pproc.children(recursive=True)
            except psutil.NoSuchProcess:
                break

            if len(children) > self._child_limit and self._child_limit != -1:
                self.exception = ProcessChildLimitHitError()
                self.terminate_process()

            all_processes = [self._pproc] + list(children)
            rss, vms = 0, 0
            for p in all_processes:
                try:
                    mem = p.memory_info()
                    rss += mem[0]
                    vms += mem[1]
                except psutil.NoSuchProcess:
                    pass

            if (rss > self._memory_limit or vms > self._memory_limit) and self._memory_limit != -1:
                self.exception = ProcessOutOfMemoryError()
                self.terminate_process()

            time.sleep(self._polling)

    def terminate_process(self):
        try:
            children = self._pproc.children(recursive=True)
        except psutil.NoSuchProcess:
            return
        
        all_processes = [self._pproc] + list(children)
        for p in all_processes:
            try:
                p.kill()
            except psutil.NoSuchProcess:
                pass

def read_from_start(file):
    file.seek(0)
    return file.read()

class ExecuteResult:
    def __init__(self, retval, out, err, exception):
        self.retval = retval
        self.stdout = out
        self.stderr = err
        self.exception = exception

    def __repr__(self):
        return f"result: {self.retval}, {self.exception}\nstdout:\n{self.stdout}\nstderr:\n{self.stderr}"

def execute(args, working_dir, shell=False, timeout=None, env_add={}, child_limit=-1, memory_limit=constants.MAX_VIRTUAL_MEMORY):
    with TemporaryFile() as err, TemporaryFile() as out:
        env = {**os.environ.copy(), **env_add}

        if constants.IS_WINDOWS or not pwd_imported:
            proc = subprocess.Popen(args, cwd=working_dir, stderr=err, stdout=out, shell=shell, env=env)
        else:
            env, demote = setup_demotion(working_dir, env)
            proc = subprocess.Popen(args, cwd=working_dir, stderr=err, stdout=out, shell=shell, env=env, preexec_fn=demote)
        
        watch = ProcessWatch(proc, memory_limit=memory_limit, child_limit=child_limit)
        watch.start()

        exception = None

        try:
            retval = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired as e:
            proc.kill()
            retval = None
            exception = e
        
        out_raw = read_from_start(out)
        err_raw = read_from_start(err)

        watch.join()
        if watch.exception:
            exception = watch.exception
        
        try:
            return ExecuteResult(
                retval,
                decoder(out_raw),
                decoder(err_raw),
                exception
            )
        except:
            return ExecuteResult(
                retval,
                dumb_decoder(out_raw),
                dumb_decoder(err_raw),
                exception
            )


def feedback_to_tests(test, index):
    if 'questions' not in test:
        return [{
                "name": test["type"],
                "score": round(test["mark"] * test["weight"] * 100, 2),
                "max_score": round(test["weight"] * 100, 2),
                "output": test["feedback"],
                "number": str(index)
            }]
    return [
            {
                "name": f'functionality - {question["question"].replace("_", " ")}',
                "score": round(float(question["mark"]) * question["weight"] * test["weight"] * 100, 2),
                "max_score": round(question["weight"] * test["weight"] * 100, 2),
                "output": question["feedback"],
                "number": f"{index}.{i + 1}"
            }
            for i, question in enumerate(test["questions"])
        ]

# Create the feedback.json file in correct format
def create_feedback_json(fb_array):
    dictionary = {
        "tests": [ item.to_dict() for item in fb_array ]
    }

    return dictionary

def save_feedback_file(dictionary, filename="result.json", verbose=False, callback=None):
    f = json.dumps(dictionary, indent=4)
    if callback and not callback(f): return
    
    with open(filename, "w+") as ofile:
        ofile.write(f)
    if verbose: print(f"Saved result to {os.path.abspath(filename)}")

def get_current_dir():
    origin = sys._getframe(1) if hasattr(sys, "_getframe") else None
    return os.path.dirname(os.path.abspath(inspect.getfile(origin)))


def dict_to_namedtuple(mapping):
    if isinstance(mapping, Mapping):
        for key, value in mapping.items():
            mapping[key] = dict_to_namedtuple(value)
        return namedtuple_from_mapping(mapping)
    return mapping

def namedtuple_from_mapping(mapping, name="Tupperware"):
    this_namedtuple_maker = namedtuple(name, mapping.keys())
    return this_namedtuple_maker(**mapping)

def get_files_in_dir(dir_path):
    assert dir_path.is_dir()
    return [f for f in dir_path.glob('**/*') if f.is_file()]

def as_md_code(lines):
    return "```\n{}\n```".format('\n'.join(lines))

class ConfigTools:
    @staticmethod
    def get_memory_limit(config, default=constants.MAX_VIRTUAL_MEMORY):
        extensions = {"": 1, "_kb": 1024, "_mb": 1024 * 1024}
        return ConfigTools._get_with_extensions(config, "memory_limit", default, extensions)
        

    @staticmethod
    def get_timeout(config, default=constants.EXECUTABLE_TIMEOUT):
        extensions = {"": 1, "_sec": 1, "_min": 60, "_ms": 0.001}
        return ConfigTools._get_with_extensions(config, "timeout", default, extensions)

    @staticmethod
    def _get_with_extensions(config, name, default, extensions):
        vals = [getattr(config, f"{name}{extension}") * multiplier 
                for extension, multiplier in extensions.items()
                if hasattr(config, f"{name}{extension}")]
        if len(vals) <= 0:
            return default
        val = min(vals)
        if val < 0:
            return -1
        return val