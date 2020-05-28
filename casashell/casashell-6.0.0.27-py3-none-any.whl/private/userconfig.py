try:
    from casaconfig import *
except:
    import os
    try:
        exec(open(os.path.expanduser("~/.casa/config.py")).read( ))
    except IOError:
        print("no ~/.casa/config.py to read")
        pass
    except:
        import traceback
        traceback.print_exc( )
        print("evaluation of ~/.casa/config.py failed")
