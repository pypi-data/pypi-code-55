###
### add configuration files for casatools and casatasks
###
import sys
from casashell.private import config
from casashell import argv
sys.path.append(config.internal_configpath)

###
### This is not so great. The configuration is set up outside of our ipython instance.
### This means that we must traverse back and pull in the configuration to make it
### available (not only for the CASA users and scripts, but also to configure
### casatools and casatasks...
###
def __incfg__( ):
    import config as newcfg
    import casatoolrc as newtool
    import casataskrc as newtask
    import inspect
    origcfg = None
    frame = inspect.currentframe( )
    while frame is not None:
        if 'casa_config_master' in frame.f_locals:
            origcfg = frame.f_locals['casa_config_master']
            break
        frame = frame.f_back

    if origcfg is None:
        import os
        print("configuration initalization failed")
        os._exit(1)
    else:
        for cfg in dir(origcfg):
            if cfg == 'datapath' and origcfg.datapath is not None:
                newtool.datapath = origcfg.datapath
                newcfg.datapath = origcfg.datapath
            elif cfg == 'logfile' and origcfg.logfile is not None:
                newtask.logfile = origcfg.logfile
                newcfg.logfile = origcfg.logfile
            elif not cfg.startswith('_'):
                setattr(newcfg,cfg,getattr(origcfg,cfg))

__incfg__( )

###
### ensure that the CASA modules are available within the shell
###
import casatools
import casatasks

###
### import legacy tools if available...
###
try:
    import casalith
except:
    pass

try:
    from casalith import browsetable
except:
    pass

try:
    from almatasks import wvrgcal
except:
    pass
try:
    from casaviewer.gotasks.imview import imview
    viewer = imview
except:
    try:
        from casaviewer import imview
        viewer = imview
    except:
        pass
try:
    from casaviewer.gotasks.msview import msview
except:
    try:
        from casaviewer import msview
    except:
        pass
try:
    from casaplotms.gotasks.plotms import plotms
except:
    try:
        from casaplotms import plotms
    except:
        pass

###
### start logger if the executable can be found and the log file
### is writable... (this will need to be adjusted for MacOS)
###
if '--nologger' not in argv:
    from shutil import which
    logger = which('casalogger')
    if logger is not None:
        import os
        log = casatools.logsink( ).logfile( )
        if os.access( log, os.W_OK ):
            import subprocess 
            import atexit
            try:
                p = subprocess.Popen([logger,log])
                def stop_logger( ):
                    p.kill( )
                atexit.register(stop_logger)
            except:
                pass

###
### execfile(...) is required by treaties and obligations (CAS-12222), but
### only in CASAshell...
###
def execfile(filename,globals=globals( ),locals=None):
    from runpy import run_path
    newglob = run_path( filename, init_globals=globals )
    for i in newglob:
        globals[i] = newglob[i]

###
### evaluate scriptpropogating errors out of ipython
###
def __evprop__(args):
    import os
    import sys
    from runpy import run_path
    exit_status = None
    if len(args) > 0:
        try:
            if os.path.isfile(args[0]):
                import sys
                exec_globals = globals( )
                exec_globals['sys'].argv = args
                run_path( args[0], init_globals=exec_globals, run_name='__main__' )
            else:
                for stmt in args:
                    exec(stmt)
        except SystemExit as err:
            exit_status = { 'code': err.code, 'desc': 'system exit called' }
        except:
            import traceback
            traceback.print_exc(file=sys.stderr)
            exit_status = { 'code': 1, 'desc': 'exception: %s' % sys.exc_info()[0] }
    else:
        exit_status = { 'code': 1, 'desc': 'no file or statement' }

    if exit_status is not None:
        import inspect
        frame = inspect.currentframe( )
        while frame is not None:
            if 'casa_eval_status' in frame.f_locals and \
               type(frame.f_locals['casa_eval_status']) is dict:
                status = frame.f_locals['casa_eval_status']
                for k in exit_status:
                    status[k] = exit_status[k]
                break
            frame = frame.f_back

###
### set the CASA prompt
###
from IPython.terminal.prompts import Prompts, Token

class _Prompt(Prompts):
     def in_prompt_tokens(self, cli=None):
         return [(Token.Prompt, 'CASA <'),
                 (Token.PromptNum, str(self.shell.execution_count)),
                 (Token.Prompt, '>: ')]

_ip = get_ipython()
try:
    ## generally thought to make tab completion faster...
    _ip.Completer.use_jedi = False
except: pass

_ip.prompts = _Prompt(_ip)
