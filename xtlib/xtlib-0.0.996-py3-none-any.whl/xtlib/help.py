# xt_help.py - contains help messages for the command line version of XT.

import sys
from .utils import BUILD

def get_short_help():
    text = f'''
XTLib ({BUILD})
    
XT is a command line tool for tracking and scaling ML experiments, using Azure Storage and Batch services.

Common commands:
    - xt help                           # display 'about XTLib' page 
    - xt help cmds                      # display a list of all XT commands and options 
    - xt config                         # view or edit the XT config file settings
    - xt python <filename> <app args>   # run python on file (with run logging) on local machine
    - xt list runs [ <name list> ]      # list all (or matching) runs in current workspace
'''
    return text

def get_about_help():
    text = f'''
XTlib ({BUILD})
Experiment Tools Library

XTlib is an API and command line tool for running and managing ML experiments.  

Features:
    - Experiment Store (local machine, server, Azure Storage)
        - centralized storage of experiment logs, source files, results, and models
        - management of workspaces (add ws, add collaborators, delete ws, enumerate)
        - management of experiments (add, annotate, delete, copy, extract, enumerate)
        - management of workspace and experiment files (upload, download, enumerate)

    - Experiment Run (local machine, server, Azure VM, Azure Batch)
        - start new experiment on specified machine(s)
        - stop run
        - check / monitor status of run
        - annotate run (comments)
        - log events
        - hyperparameter tuning runs

The goal of XTLib is to enable you to effortlessly organize and scale your ML experiments.
Our tools offer an incremental approach to adoption, so you can begin realizing benifits immediatly.

XTLib provides an experiment STORE that enables you to easily track, compare, rerun, and share your ML experiments.  
The STORE consists of user-defined workspaces, each of which can contain a set of user-run experiments.  
XT currently supports 2 STORE services: local (folder-based) and azure (Azure Storage-based).

In addition, XTLib also provides simple access to scalable COMPUTE resources so you can 
easily run multiple experiments in parallel and on larger computers, as needed.  With this feature, 
you can run your experiments on your local machine, other local computers or provised VMs to which you 
have aceess, or on 1 or more cloud computers, allocated on demand (Azure Batch).

For more information, run: xt help cmds'''

    return text

def get_api_help():
    text = '''
XTLib API 
The XTLib API is defined in 3 primary modules:
    - xt_store
    - xt_compute
    - xt_client

The xt_store module implements create, log, list, update, delete type operations for the user's workspaces, 
experiments, and files associated with both of these.

The xt_compute modules allows a program to start and managing the running of experiments.

The xt_client module contains additional features needed by the XT command line tool.

The XT command line app is built directly on top of the these modules.  You can use the XTLib API to 
add workspace and experiment functionality to your app.  Typical usages include:
    - logging ML progress and final scores
    - logging experiment hyperparameters
    - reading and writing experiment-related files
    - launching, controlling, and stopping experiments 

XTLib Low Level API
The xt_store and xt_compute are implemented using 5 additional modules:
    - xt_store_file   (implements the XT STORE API using local file-based storage)
    - xt_store_blob   (implements the XT STORE API using Azure Storage blobs and containers)
    - xt_compute_local  (implements the XT COMPUTE API using the local machine)
    - xt_compute_box  (implements the XT COMPUTE API using box machines (peer or provisioned VM's))
    - xt_azure_batch  (implements the XT COMPUTE API using the Azure Batch service) '''

    return text

def color_print_lines(text):
    gray = "\033[0;37m"
    #white = "\033[1;37m"
    darkgray = "\033[1;30m"
    reset = "\033[0m"
    bold_on = "\033[106;0;1m"
    bold_off = "\033[106;0;0m"

    for line in text.split("\n"):
        if line.startswith("z"):
            sys.stdout.write(bold_on)
            print(line[1:])
            sys.stdout.write(bold_off)
        elif line.startswith("x"):
            #sys.stdout.write(darkgray)
            print(line[1:])
            #sys.stdout.write(reset)
        else:
            print(line)

def get_cmd_help():

    text = '''
usages: 
     xt [ <dashed options> ] python <python file and command line arguments>
     xt [ <dashed options> ] run <app file and command line arguments>
     xt [ <dashed options> ] <command>  [ <undashed options> ]

note: command keywords can be abbreviated down to 4 letters

general:
     - xt                   # display XT about information
     - xt config            # edit/view the config file settings
     - xt help [ <value> ]  # displays XT commands and options (value can be 'cmds', 'about', or 'api')
     - xt version           # display the version number and build date of XT
     - xt repl              # turn on XT's REPL mode (use "repl" to toggle this off)

runs - control:
     - xt python <filename> <app args>          # run python on file (under control of xt)
     - xt run app <app args>                    # run the app (under control of xt)
     - xt docker run <args>                     # run the specified docker image (under control of xt)
     - xt kill <name list>                      # terminates the run(s) specified by the run, experiment, or box
     - xt rerun <name> [ <app args> ]           # rerun the specified run with optional new cmd args

runs - information:
     - xt status [ <name> ]                     # display the current runs on the local or specified box/pool
     - xt attach <name>                         # attach output of run to console (use ESC to detach)
     - xt list runs [ <name list> ]             # list all (or matching) runs in current workspace

general information:
     - xt list experiments [ <name> ]           # list all (or matching) experiments in current workspace
     - xt list jobs [ <wildcard name> ]         # list all jobs in store
     - xt list boxes [ <wildcard name> ]        # list all boxes defined in config file
     - xt list pools [ <wildcard name> ]        # list all pools defined in config file
     - xt view console <name>                   # view console output from run (after it has finished running)
     - xt view log <name>                       # view live log of run name or "controller"
     - xt view metrics <name>                   # view the metrics logged for the specified run
     - xt plot <name list>                      # display a line plot for the metrics of the specified runs
     - xt extract <name> to <output directory>  # copy the specified run from the store to a local directory
     - xt explore <name>                        # run hyperparameter explorer on specified experiment
     - xt dir [ <path> ]                       # show contents of store
     - xt cat [ <path> ]                       # display contents of store file
     - xt addr <box name or pool>           # display the address for the specified box(es)

workspaces:
     - xt list workspaces                   # list workspaces 
     - xt create workspace <name            # create new workspace
     - xt delete workspace <name>           # delete the specified workspace

file shares:
     - xt upload file from <local path> to <path>         # upload local file to share path
     - xt download file from <path> to <local path>       # download file from share to local
     - xt delete file <share path>                        # delete file from share
     - xt list files <share path>                         # list share files 
     
settings:
     - xt workspace                          # display the default workspace
     - xt max-runs                           # display max-runs for the specified/default box

keypair generation and distribution:
     - xt keygen                            # generate a new keypair (calls ssh-keygen, dest = ~/.ssh/xt_id_rsa)
     - xt keysend <box name>                # send public half of xt keypair files to specified box/pool

utility commands:
     - xt kill controller                   # kill the controller on the specified box
     - xt restart controller [ visible ]    # kill and restart the controller on the specified box
     - xt ssh <box> [ <cmd> ]               # opens a remote SSH session with specified box (or runs cmd if specified)
     - xt docker login                      # log docker into the Azure Container Registry from xt config file
     - xt docker logout                     # log docker out of the Azure Container Registry from xt config file

debugging / utility options:
     --diagnostics <bool>                   # turn XT diagnostics msgs on/off
     --raise                                # if an exception is caught, raise it so we can see stack trace info
     --timing <bool>                        # turn XT timing msgs on/off

general options:  
     --help                          # print detailed help
     --log <bool>                    # override logging run to STORE 
     --capture <value>               # override capturing files for this run (none, before, after, all)
     --omit <value>                  # omit specified wildcard files from being captured
     --before-files <value>          # file names (wildcard) to capture to before folder in run store
     --after-files <value>           # file names (wildcard) to capture to after folder in run store
     --notes <value>                 # override when to prompt user for notes (none, before, after, all)
     --experiment <name>             # specifies/overrides the experiment name 
     --box <name>                    # run the job on the specified box name (from config file)
     --pool <name>                   # run the job on the specified pool of boxes (from config file or 'azure-batch')
     --job <name>                    # filter the runs by those matching the specified job name
     --store <type>                  # override the STORE type (local, azure, aml) 
     --hold                          # after run has completed, holds the allocated computer open for debugging
     --description <value>           # specify a description to log with the run being launched
     --max-runs=<number>             # limit number of simultaneious instances of the app on the specified box
     --repeat <value>                # create N specified instances of the run on each box (N=-1 means to repeat forever)
     --runs=<number>                 # specify total number of runs to generate (used for hyperparm search, etc.)
     --dry-run                       # show what would be run, but don't actual start the runs
     --scrape <bool>                 # override scrape of stdout for progress and final metric 
     --workspace <name>              # override the default workspace name 
     --overwrite                     # override the existing item (keygen cmd)
     --repair <bool>                 # repair phantom runs (use with list runs cmd)
     --vm-size <name>                # override azure machine type for azure batch
     --azure-image <name>            # override azure os image name for azure batch
     --nodes <value>                 # override number of azure-batch nodes
     --low-pri <value>               # override number of low-priority (preemptable) azure-batch nodes
     --subdirs [ <value> ]           # used for dir cmd to include/limit subdirectories
     --arg-prefix <string>           # specify the "--" type prefix for cmdline args to your app
     --resume <name>                 # resume an interrupted run
     --keep-name <bool>              # specify if original run_name should be used for a --resume run 
     --demand-mode                   # internal testing option for local simulation of how xt controller runs on azure batch
     --auto-start                    # when set to true, 'status' cmd will automatically start the controller, if needed
     --hp-config <file>              # specify config file for hyperparameter searching
     --search-type <value>           # type of hyperparameter search to perform: "random" or "grid" (default=random)
     --xtlib-capture <bool>          # capture XTLIB source files from local machine and use in controller & ML app 
     --local <bool>                  # when specified, 'xt config' will edit the local overrides file
     --tqdm-enabled <bool>           # when true, will use tqdm progress bar while downloading files
     --login <bool>                  # when true, XT will log docker into ACR before the docker run is executed 
     --distributed <bool>            # when true, the target app is run as a distributed job in the specified pool

report options:
     --detail                        # one of: names, counts, cols, report
     --flat                          # list all runs without grouping them by experiment
     --sort <col name>               # default column sort for list
     --reverse <bool>                # if list sort should be reversed in order
     --escape <value>                # breaks out of attach or --monitor loop after specified # of seconds
     --boxout                        # shows only the latest runs on each box
     --monitor                       # refresh list every second
     --max-width <number>            # set max width for any column
     --precision <number>            # set number of fractional digits to show for float values
     --first [ <number> ]            # limit items shown to the first N
     --last [ <number> ]             # limit items shown to the last N

     --active                        # only list runs with status of queued, spawning, or running
     --finished                      # only list runs with status of completed, error, killed
     --queued                        # only list runs that are waiting in the queue to be started
     --spawning                      # only list repeat runs that are currently spawing another run
     --running                       # only list runs that are currently running
     --killed                        # only list runs that have been killed by the user
     --aborted                       # only list runs that unexpected terminiated (box reboot or controller restart)
     --error                         # only list runs that ended with a non-zero exit code
     --completed                     # only list runs that ran successfully to completion
     --unknown                       # only list runs whose status is 'unknown' (usually a deleted azure/normal job)

hyperparameter search notation (use in program's command line arguments):
      name=[ <value list> ]                       # specify list of discrete values for hyperparmeter
      name=[ <min> : <max> ]                      # specify min and max range of values for hyperparmeter (uniform sampling)
      name=[ <min> : <max> : <mean> : <stddev> ]  # specify min/max/mean/stddev for hyperparmeter (normalized sampling)

      Note: arg values / option must be quoted if spaces are used between values
'''
    return text
