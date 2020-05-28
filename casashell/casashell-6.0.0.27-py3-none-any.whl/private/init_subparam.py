from casashell.private.stack_manip import find_local as __sf__

def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate


@static_var("state", __sf__('casa_inp_go_state'))
def inp(obj=None):
    if obj is not None:
        if 'inp' in dir(obj):
            inp.state['last'] = obj
            obj.inp( )
        else:
            print("ERROR %s does not seem to be a CASA task" % obj)
    elif 'last' in inp.state and inp.state['last'] is not None:
        inp.state['last'].inp( )
    else:
        print("ERROR task argument needed")

@static_var("state", __sf__('casa_inp_go_state'))
def go(obj=None):
    if obj is not None:
        if 'inp' in dir(obj):
            go.state['last'] = obj
            return obj( )
        else:
            print("ERROR %s does not seem to be a CASA task" % obj)
            return None
    elif 'last' in go.state and go.state['last'] is not None:
        return go.state['last']( )
    else:
        print("ERROR task argument needed")
        return None

def default(obj):
    if 'set_global_defaults' in dir(obj):
        obj.set_global_defaults( )
        return True
    else:
        print("ERROR argument does not appear to be a task")
        return False

def tget(obj=None,file=None):
    if obj is not None:
        if 'tget' in dir(obj):
            obj.tget( )
            return True
        else:
            print("ERROR 'obj' argument does not appear to be a task")
            return False
    elif file is not None:
        if isinstance(file, str):
            import os
            if os.path.isfile(file):
                from .stack_manip import find_frame
                from runpy import run_path
                glob = find_frame( )
                newglob = run_path( file, init_globals={ } )
                for i in newglob:
                    glob[i] = newglob[i]
                    return True
            else:
                print("ERROR 'file' argument (%s) is not a file" % file)
                return False
        else:
            print("ERROR 'file' argument should be a string")
            return False
    else:
        print("ERROR tget requires either a file to load or a task")
        return False
        
del __sf__
del static_var
