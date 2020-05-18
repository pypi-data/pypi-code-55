"""basic functions used to modify and read scikick.yml"""
import os
import re
import sys
import ruamel.yaml as yaml
from scikick.utils import reterr, warn

def file_noex_msg(fname):
    """Check whether 'fname' is a file, exit with a
    non-zero return code if it is not.
    fname -- string (filename)
    """
    if os.path.isdir(fname):
        reterr("sk: Error: Can add only files, directory given")
    else:
        warn("sk: Warning: File \'%s\' does not exist, creating it now" % \
            fname)
        warn("sk: touch %s" % fname)
        if not os.system("touch %s" % fname) == 0:
            sys.exit(1)

def yaml_dump(ymli):
    """Write a dictionary to scikick.yml.
    ymli -- dict
    """
    ymlo = yaml.YAML()
    ymlo.dump(ymli, open("scikick.yml", "w"))

def yml_in(ymlpath='scikick.yml'):
    """Read scikick.yml.
    Returns an ordereddict.
    """
    #Exit with an error message if scikick.yml is not found
    if not os.path.isfile(ymlpath):
        reterr(f"sk: Error: {ymlpath} not found," + \
               "to get a template, run\nsk: sk init")

    ymli = yaml.YAML()
    ymli = ymli.load(open(ymlpath, "r"))
    return ymli

def rename(name_a, name_b):
    """Rename file 'a' in scikick.yml to 'b'
    a -- string (filename)
    b -- string (filename)
    """
    found = 0
    ymli = yml_in()
    ## rename keys (ana)
    if name_a in ymli["analysis"].keys():
        ymli["analysis"][name_b] = ymli["analysis"].pop(name_a)
        found = 1
    ## rename values (deps)
    if ymli["analysis"] is not None:
        for k in ymli["analysis"].keys():
            if ymli["analysis"][k] is not None and \
                name_a in ymli["analysis"][k]:
                ymli["analysis"][k][ymli["analysis"][k].index(name_a)] = \
                    name_b
                found = 1
    yaml_dump(ymli)
    return found

def set_arg(arg, val):
    """Set value of 'arg' in scikick.yml to 'val'.
    Result: scikick.yml:
    <...>
    arg: val
    <...>
    arg -- string
    val -- string
    """
    ymli = yml_in()
    ymli[arg] = val
    warn("sk: Argument \'%s\' set to \'%s\'" % (arg, val))
    yaml_dump(ymli)

def get_arg(arg):
    """Read value of field 'arg' in scikick.yml.
    Returns a string
    arg -- string
    """
    ymli = yml_in()
    if arg in ymli.keys():
        return ymli[arg]
    return ""

def set_snakeargs(snakeargs):
    """Set 'snakeargs' field in scikick.yml
    snakeargs -- string
    """
    ymli = yml_in()
    ymli['snakemake_args'] = snakeargs
    yaml_dump(ymli)

def get_snakeargs():
    """Get the value of 'snakeargs' field from scikick.yml"""
    ymli = yml_in()
    if 'snakemake_args' in ymli.keys():
        return " ".join(ymli['snakemake_args'])
    return ""

def add_file(fname):
    """Add file 'fname' to 'analysis' dict in scikick.yml
    fname -- string (filename)
    """
    if not os.path.isfile(fname):
        file_noex_msg(fname)
    # check if rmd
    if not re.match(".*.Rmd", fname, re.I):
        reterr("sk: Error: only .Rmd files can be added")
    ymli = yml_in()
    if ymli['analysis'] is None:
        ymli['analysis'] = {}
    if fname in ymli['analysis'].keys():
        warn("sk: \'%s\' is already included" % fname)
    else:
        ymli['analysis'][fname] = None
        warn("sk: Added \'%s\'" % fname)
    yaml_dump(ymli)

def rm_file(fname):
    """Remove file 'fname' from 'analysis' dict in scikick.yml
    fname -- string (filename)
    """
    ymli = yml_in()
    if ymli['analysis'] is None:
        warn("sk: Warning: Nothing to remove")
        return
    if fname in ymli['analysis'].keys():
        del ymli['analysis'][fname]
        warn("sk: \'%s\' removed" % fname)
    else:
        warn("sk: Warning: File \'%s\' not included" % fname)
    yaml_dump(ymli)

def add_dep(ana_name, dep):
    """Add a dependency 'dep' to file 'ana_name'
    in 'analysis' dict, scikick.yml
    ana_name -- string (filename)
    dep -- string (filename)
    """
    if not os.path.isfile(ana_name):
        file_noex_msg(ana_name)
    ymli = yml_in()
    if ymli['analysis'] is None:
        ymli['analysis'] = {}
    if ana_name not in ymli['analysis'].keys():
        warn("sk: Warning: \'%s\' was not included, adding now" % ana_name)
    if ana_name not in ymli['analysis'].keys() or\
        ymli['analysis'][ana_name] is None:
        ymli['analysis'][ana_name] = []
    if not os.path.isfile(dep):
        warn("sk: Warning: \'%s\' does not exist or is not a file" % dep)
    if dep in ymli['analysis'][ana_name]:
        warn("sk: \'%s\' is already a dependency of \'%s\'" % (dep, ana_name))
    else:
        ymli['analysis'][ana_name].append(dep)
        warn("sk: Added dependency \'%s\' to \'%s\'" % (dep, ana_name))
    yaml_dump(ymli)

def rm_dep(ana_name, dep):
    """Remove a dependency 'dep' from file 'ana_name'
    in 'analysis' dict, scikick.yml
    ana_name -- string (filename)
    dep -- string (filename)
    """
    ymli = yml_in()
    if ymli['analysis'] is None or \
        ana_name not in ymli['analysis'].keys() or \
        ymli['analysis'][ana_name] is None:
        reterr("sk: Error: Nothing to remove")
    if dep in ymli['analysis'][ana_name]:
        ymli['analysis'][ana_name].remove(dep)
        warn("sk: \'%s\' removed from \'%s\'" % (dep, ana_name))
    else:
        warn("sk: \'%s\' is not in analysis \'%s\'" % (dep, ana_name))
    if len((ymli['analysis'][ana_name])) == 0:
        ymli['analysis'][ana_name] = None
    yaml_dump(ymli)
