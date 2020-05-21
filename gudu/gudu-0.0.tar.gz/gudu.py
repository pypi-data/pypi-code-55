import platform
import os
from pip import _internal

def me():
    print(os.name)
    print(platform.system())
    print(platform.release())

def superme():
    # Architecture
    print("Architecture: " + platform.architecture()[0])
    
    # machine
    print("Machine: " + platform.machine())
    
    # node
    print("Node: " + platform.node())
    
    # system
    print("System: " + platform.system())

def proc():
    # processor
    #print("Processors: ")
    #with open("/proc/cpuinfo", "r")  as f:
    #    info = f.readlines()
        
    #cpuinfo = [x.strip().split(":")[1] for x in info if "model name"  in x]
    #for index, item in enumerate(cpuinfo):
    #    print("    " + str(index) + ": " + item)
    print('Processor(s)')

def mem():
    # Memory
    #print("Memory Info: ")
    #with open("/proc/meminfo", "r") as f:
    #    lines = f.readlines()
    #    print("     " + lines[0].strip())
    #    print("     " + lines[1].strip())
    print('Memory Usage')

def plist():
    _internal.main(['list'])

#me()
#superme()
#proc()
#mem()
plist()