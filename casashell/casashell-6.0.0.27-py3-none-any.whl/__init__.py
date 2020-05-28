import os as _os
import sys as _sys
import argparse as _argparse
from traitlets.config.loader import Config

__name__ = 'casashell'
__all__ = [ "start_casa", "argv", "version", "version_string", "extra_task_modules" ]

extra_task_modules = [ ]

def version( ): return [ 6, 0, 0,27 ]
def version_string( ): return "6.0.0.27"

argv = _sys.argv

def __init_config(config,flags,args):
    if flags.datapath is not None:
        datap = list(map(_os.path.abspath,filter(_os.path.isdir,list(flags.datapath.split(':')))))
        config.datapath = datap
    if flags.logfile is not None:
        config.logfile = flags.logfile if flags.logfile.startswith("/") else _os.path.realpath(_os.path.join('.',flags.logfile))

    config.flags = flags
    config.args = args
                
def start_casa( argv ):
    from .private import config
    from IPython import start_ipython
    moduledir = _os.path.dirname(_os.path.realpath(__file__))

    ###
    ### this will be used by inp/go which are introduced in init_subparam
    ###
    casa_inp_go_state = { 'last': None }

    ###
    ### this will be used by register_builtin for making casa builtins immutable
    ###
    casa_builtin_state = { }
    casa_nonbuiltin_state = { }    ### things that should be builtin but are not

    ##
    ## this is filled via add_shutdown_hook (from casa_shutdown.py)
    ##
    casa_shutdown_handlers = [ ]

    ##
    ## filled when -c <args> is used
    ##
    casa_eval_status = { 'code': 0, 'desc': 0 }

    init_scripts = [ "init_system.py",
                     "load_tasks.py",
                     "load_tools.py",
                     "init_subparam.py",
                     "init_doc.py",
    ]

    if _os.path.isfile(_os.path.expanduser("~/.casa/startup.py")):
        init_scripts += [ _os.path.expanduser("~/.casa/startup.py") ]

    init_scripts += [ "init_welcome.py" ]

    ##
    ## final interactive exit status...
    ## runs using "-c ..." exit from init_welcome.py
    ##
    _exit_status=0
    try:
        startup_scripts = filter( _os.path.isfile, map(lambda f: _os.path.join(moduledir,"private",f), init_scripts ) )

        parse = _argparse.ArgumentParser(description='CASA bootstrap',add_help=False)
        parse.add_argument( '--logfile',dest='logfile',default=None,help='path to log file' )
        parse.add_argument( "--maclogger",dest='maclogger',action='store_const',const='console',
                            default='/does/this/still/make/sense',
                            help='logger to use on Apple systems' )
        parse.add_argument( "--log2term",dest='log2term',action='store_const',const=True,default=False,
                            help='direct output to terminal' )
        parse.add_argument( "--nologger",dest='nologger',action='store_const',const=True,default=False,
                            help='do not start CASA logger' )
        parse.add_argument( "--nologfile",dest='nologfile',action='store_const',const=True,default=False,
                            help='do not create a log file' )
        parse.add_argument( "--nogui",dest='nogui',action='store_const',const=True,default=False,
                            help='avoid starting GUI tools' )
        parse.add_argument( '--colors', dest='prompt', default='NoColor',
                            help='prompt color', choices=['NoColor', 'Linux', 'LightBG'] )
        parse.add_argument( "--trace",dest='trace',action='store_const',const=True,default=False,
                            help='list imported modules' )
        parse.add_argument( "--pipeline",dest='pipeline',action='store_const',const=True,default=False,
                            help='start CASA pipeline run' )
        parse.add_argument( "--agg",dest='agg',action='store_const',const=True,default=False,
                            help='startup without graphical backend' )
        parse.add_argument( '--iplog',dest='ipython_log',default=False,
                            const=True,action='store_const',
                            help='create ipython log' )
        parse.add_argument( '--datapath',dest='datapath',default=None,
                            help='data path(s) [colon separated]' )
        parse.add_argument( '--nocrashreport',dest='crash_report',default=True,
                            const=False,action='store_const',
                            help='do not submit an online report when CASA crashes' )
        parse.add_argument( '--telemetry',dest='telemetry',default=False,
                            const=True,action='store_const',
                            help='Enable telemetry collection' )
        parse.add_argument( "-c",dest='execute',default=[],nargs=_argparse.REMAINDER,
                            help='python eval string or python script to execute' )
        flags,args = parse.parse_known_args( )

        from .private import config
        casa_config_master = config
        __init_config(casa_config_master,flags,args)

        from IPython import __version__ as ipython_version
        configs = Config( )
        configs.TerminalInteractiveShell.ipython_dir = _os.path.join(config.rcdir,"ipython")
        configs.TerminalInteractiveShell.banner1 = 'IPython %s -- An enhanced Interactive Python.\n\n' % ipython_version
        configs.TerminalInteractiveShell.banner2 = ''
        configs.HistoryManager.hist_file = _os.path.join(configs.TerminalInteractiveShell.ipython_dir,"history.sqlite")
        configs.TerminalIPythonApp.matplotlib = 'agg' if flags.agg or flags.pipeline else 'auto'
        configs.InteractiveShellApp.exec_files = list(startup_scripts)

        import casashell as _cs
        _cs.argv = argv
        _os.makedirs(_os.path.join(config.rcdir,"ipython"),exist_ok=True)
        start_ipython( config=configs, argv= (['--logfile='+config.iplogfile] if flags.ipython_log else []) + ['--ipython-dir='+_os.path.join(config.rcdir,"ipython"), '--autocall=2'] + (["-i"] if len(flags.execute) == 0 else ["-c","__evprop__(%s)" % flags.execute]) )

    except:
        casa_eval_status['code'] = 1
        casa_eval_status['desc'] = "unexpected error"
        pass

    ### this should (perhaps) be placed in an 'atexit' hook...
    for handler in casa_shutdown_handlers:
        handler( )

    #from init_welcome_helpers import immediate_exit_with_handlers
    #immediate_exit_with_handlers(_exit_status)
    return casa_eval_status['code']
