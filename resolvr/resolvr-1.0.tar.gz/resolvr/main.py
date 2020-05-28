#!/usr/bin/env python

#Application imports.
import sys,signal,netaddr,json,requests,socket

from resolvr import VERSION, PROG_NAME, PROG_DESC, PROG_EPILOG, DEBUG

#Try to import argparse, not available until Python 2.7
try:
    import argparse
except ImportError:
    print_err("Failed to import argparse module. Needs python 2.7+.")
    quit()
#Try to import termcolor, ignore if not available.
DO_COLOR = True
try:
    import termcolor
except ImportError:
    DO_COLOR = False
def try_color(string, color):
    if DO_COLOR:
        return termcolor.colored(string, color)
    else:
        return string
#Print some info to stdout
def print_info(*args):
    sys.stdout.write(try_color("info: ", "green"))
    sys.stdout.write(try_color(" ".join(map(str,args)) + "\n", "green"))
#Print an error to stderr
def print_err(*args):
    sys.stderr.write(try_color("error: ", "red"))
    sys.stderr.write(try_color(" ".join(map(str,args)) + "\n", "red"))
#Print a debug statement to stdout
def print_debug(*args):
    if DEBUG:
        sys.stderr.write(try_color("debug: ", "blue"))
        sys.stderr.write(try_color(" ".join(map(str,args)) + "\n", "blue"))
#Handles early quitters.
def signal_handler(signal, frame):
    print("")
    quit(0)

# Argument parsing which outputs a dictionary.
def parseArgs():
    #Setup the argparser and all args
    parser = argparse.ArgumentParser(prog=PROG_NAME, description=PROG_DESC, epilog=PROG_EPILOG)
    parser.add_argument("-v", "--version", action="version", version="%(prog)s " + VERSION)
    parser.add_argument("-q", "--quiet", help="surpress extra output", action="store_true", default=False)
    parser.add_argument("-i", "--input", help="input list of domains to test (default stdin)", nargs="?", type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument("-o", "--output", help="output filename", nargs="?", type=argparse.FileType('w'), default=None)
    parser.add_argument("-s", "--scope", help="input list of in-scope address ranges (default *)", nargs="?", type=argparse.FileType('r'))
    parser.add_argument("-O", "--out-of-scope", help="out of scope hosts output filename", nargs="?", type=argparse.FileType('w'), default=None)
    parser.add_argument("-n", "--no-resolve", help="non-resolved hosts output filename", nargs="?", type=argparse.FileType('w'), default=None)
    return parser.parse_args()

def print_header():
    print(r"                           ___                      ")
    print(r"                          /\_ \                     ")
    print(r" _ __    __    ____    ___\//\ \    __  __   _ __   ")
    print(r"/\`'__\/'__`\ /',__\  / __`\\ \ \  /\ \/\ \ /\`'__\ ")
    print(r"\ \ \//\  __//\__, `\/\ \L\ \\_\ \_\ \ \_/ |\ \ \/  ")
    print(r" \ \_\\ \____\/\____/\ \____//\____\\ \___/  \ \_\  ")
    print(r"  \/_/ \/____/\/___/  \/___/ \/____/ \/__/    \/_/  ")
    print(r"                                                    ")
    print(r"                                             v" + VERSION)

#Main application entry point.
def main():
    #Signal handler to catch CTRL-C (quit immediately)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    argv = parseArgs()

    #Print out some sweet ASCII art.
    if not argv.quiet:
        print_header()

    # Iterate through all passed addresses
    domains_txt = argv.input.readlines()
    argv.input.close()

    try:
        scope_txt = argv.scope.readlines()
        argv.scope.close()
    except Exception as e:
        scope_txt = ["0.0.0.0/0"]

    for domain in domains_txt:
        domain = domain.strip()

        # Handles blank lines
        if domain is "" or domain is None:
            continue

        resolved_addr = ""
        try:
            # Try to resolve the host via DNS (if already resolved, will just return)
            resolved_addr = socket.gethostbyname(domain)
        except socket.gaierror as err:
            print_err("Failed to resolve the host %s" % (domain))
            if not argv.no_resolve is None:
                argv.no_resolve.write(domain + "\n")
            continue
        # Turn IP string into IP addr object
        ip_addr = netaddr.IPAddress(resolved_addr)

        in_scope = False
        # Iterate through all ranges in the returned AWS response
        for scope_addr_obj in scope_txt:
            scope_addr_obj = scope_addr_obj.strip()
            
            # Handles blank lines
            if scope_addr_obj is "" or scope_addr_obj is None:
                continue

            if ip_addr in netaddr.IPNetwork(scope_addr_obj):
                # Host is in scope
                in_scope = True
                break
                    
        if in_scope:
            if argv.scope:
                print_info("Host %s resolves to %s and is in scope" % (domain, resolved_addr))
            else:
                print_info("Host %s resolves to %s" % (domain, resolved_addr))
            if not argv.output is None:
                argv.output.write(resolved_addr + "," + domain + "\n")
        else:
            # Host is out of scope
            if not argv.out_of_scope is None:
                argv.out_of_scope.write(resolved_addr + "," + domain + "\n")

            if not argv.quiet:
                sys.stdout.write(try_color("info: ", "yellow"))
                sys.stdout.write(try_color("Host %s resolves to %s but is *not* in scope\n" % (domain, resolved_addr), "yellow"))


    if not argv.output is None:
        argv.output.close()
    if not argv.out_of_scope is None:
        argv.out_of_scope.close()
    if not argv.no_resolve is None:
        argv.no_resolve.close()


if __name__ == "__main__":
    main()
    quit(0)

