"""utilities for processes.
"""

import os
import subprocess
import signal

__version__="5.1" #VERSION#

# pylint: disable=invalid-name

def child_pids(pid):
    """get children pid's."""
    reply= subprocess.Popen("ps --ppid=%s -o pid=" % pid,
                            shell=True, \
                            stdout=subprocess.PIPE).communicate()[0]
    return reply.split()

# my_pid: get own process id:
my_pid= os.getpid

def write_pids(filename,pids):
    """write PID's to a file.

    parameters:
        - filename: the name of the PID file
        - pids    : a list of pairs, each pair a PID and the corresponding
                    command
    """
    fh= open(filename,"w")
    for (pid,cmd) in pids:
        fh.write("%6d %s\n" % (pid,cmd))
    fh.close()

def write_pid_cmd(pidfile, args):
    """write cmd and PID to PID file."""
    if pidfile is None:
        return
    args_= args[:]
    args_[0]= os.path.basename(args_[0])
    write_pids(pidfile, [(os.getpid(), " ".join(args_))])

def send_signal(signal_, pidfile):
    """send a signal to the process specifed by the pidfile."""
    if pidfile is None:
        return
    fh= open(pidfile,"r")
    for l in fh:
        l= l.strip()
        (pid,_)= l.split(None, 1)
        os.kill(int(pid), signal_)
    fh.close()

def kill_pids(pidfile):
    """kill all given pid's."""
    if pidfile is None:
        return
    try:
        fh= open(pidfile,"r")
    except IOError:
        return
    for l in fh:
        l= l.strip()
        (pid,_)= l.split(None, 1)
        children= child_pids(pid)
        children.append(pid)
        for p in children:
            try:
                # print "KILL process %d" % int(p)
                os.kill(int(p), signal.SIGTERM)
            except OSError:
                # catch: OSError: [Errno 3] No such process
                pass
    fh.close()
