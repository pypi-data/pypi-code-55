
import os
import sys

try:
    from pyjsoncfg import Config
except:
    from .pyjsoncfg import Config
 

VERSION="v0.0.3"

def main():
     
    import argparse
     
    parser = argparse.ArgumentParser(prog='pyjsoncfg', usage='%(prog)s [options]',
        description='sanitize json config file, details refer to https://github.com/kr-g/pyjsoncfg')
    
    parser.add_argument("-v", "--version", dest='show_version', action="store_true",
                        help="show version info and exit", default=False )
    parser.add_argument("-d", "--debug", dest='show_debug', action="store_true",
                        help="show debug info", default=False )

    parser.add_argument("-f", dest='config', action="store",
                        help="input json config file (default: %(default)s)",
                        default = Config.DEFAULT_CONFIG_FILE 
                        )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--list", dest='dont_sanitize', action="store_true",
                        help="list config, do not sanitize (default: %(default)s)",
                        default = False
                        )
    group.add_argument("-k", "-key", "-keyword", metavar= "KEYWORD", dest='keywords', action="append",
                        help="additional keyword to scan for (default: %(default)s)",
                        default=[] )

    args = parser.parse_args()
    
    if args.show_version:
        print( "Version:", VERSION )
        return
     
    base, fnam = os.path.split( args.config )
    if len(base) == 0:
        base=None

    if args.show_debug:
        print( "basedir:", base )
        print( "config file:", args.config )
        print( "keywords:", args.keywords )
     
    os.environ.setdefault(Config.PYJSONCONFIG_BASE,"~")
    
    cfg = Config(fnam, basepath=base, not_exist_ok=False, auto_conv=False )
    if not args.dont_sanitize:
        cfg.sanitize(args.keywords)
    cfg.savefd(sys.stdout)
    
    return cfg

     
if __name__=='__main__':
 
##    os.environ.setdefault("PYJSONCONFIG_BASE",".")
##    sys.argv = "pyjsonconfig -f sample_cfg.json -k secret -d -l".split()
##    sys.argv = "pyjsonconfig -f sample_cfg.json".split()
    
    cfg = main()

