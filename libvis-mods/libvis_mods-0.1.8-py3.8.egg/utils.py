import subprocess
import inspect
from inspect import Parameter
from loguru import logger as log
import shutil, os, errno

def make_sure_path_exists(path):
    """Ensure that a directory exists.
    :param path: A directory path.
    """
    log.debug("Making sure path exists: {}", path)
    try:
        os.makedirs(path)
        log.debug("Created directory at: {}", path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True

def only_required_kwargs_call(f, *args, **kwargs):
    sig = inspect.signature(f)
    of_type = lambda type: [name for name, param in sig.parameters.items()
                if param.kind == type
               ]
    pos = of_type(Parameter.POSITIONAL_OR_KEYWORD)
    #_args = of_type( Parameter.VAR_KEYWORD)
    keyw = of_type(Parameter.KEYWORD_ONLY)
    _kwargs = of_type(Parameter.VAR_KEYWORD)
    if len(_kwargs):
        return f(*args, **kwargs)
    else:
        names = pos + keyw
        print(names)
        conf = {name:value for 
                name, value in kwargs.items() if name in names
               }
        return f(*args, **conf)


def rm(obj):
    if obj.is_symlink():
        os.unlink(obj)
    elif obj.is_dir():
        shutil.rmtree(obj)
    elif obj.is_file():
        os.remove(obj)

def safe_copy(src, dest):
    if not dest.exists():
        shutil.copy(src, dest)
        return True
    else:
        return False

def copy(src, dest):
    print("cp", src, dest)
    if src.is_dir():
        src = str(src) + str(os.sep)
    run_cmd(['rsync','-r', src, dest])

def ln(src, dest):
    print("ln -sf", src, dest)
    if src.is_dir():
        src = str(src) + str(os.sep)
    try:
        run_cmd(['ln','-s', src, dest])
    except:
        print("Failed to link,skipping")

def write_to(s, dest):
    with open(dest, 'w+') as f:
        f.write(s)

def run_cmd(cmds):
    try:
        subprocess.run(cmds,
            #' '.join([str(x) for x in cmds]),
                   shell=False, check=True
                  )
    except subprocess.CalledProcessError as e:
        output, stderr = e.output, e.stderr
        if output:
            output = output.decode()
        if stderr:
            stderr = stderr.decode()
        raise Exception(f"Failed to execute `{cmds[0]}`.\n\
 Command: {e.cmd}.\n\
Output: {output}, stderr: {stderr}")
