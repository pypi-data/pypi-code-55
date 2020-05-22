#-*-coding:utf-8-*-
import os,hashlib
from .gui import (color,gui)
from .environment import cardsdkEnv

color = color()
cui = gui()

def zsmd5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# scan dir 
def tree(filepath,result):
    fileOrDirs = os.listdir(filepath)  
    for fi in fileOrDirs:    
        fi_d = os.path.join(filepath,fi)    
        if os.path.isdir(fi_d):
            tree(fi_d,result)    
        else:
            result.append(fi_d)     
    return result  

#
def getAllFtFiles(path,ft):
    results=[]
    treeResult=[]
    tree(path,treeResult)
    for f in treeResult:
        fileType=os.path.splitext(f)[-1]
        if fileType == ft:
            results.append(f)
        else:
            pass
    return results

def checkInstalled(command):
    commandPass=0
    for cmdpath in os.environ['PATH'].split(':'):
        if os.path.isdir(cmdpath) and command in os.listdir(cmdpath):
            commandPass=1
        if not commandPass:
            commandPass=0
    return commandPass

def setupEnv():
    #env setup
    print('\r\n')
    cui.w('start setup env...')
    env = cardsdkEnv()
    env.AntCardSDKSetup()
    cui.w('env is ready!')
