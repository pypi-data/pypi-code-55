"""
This code produces the NPK default parameter file from the ProcessXX python files

see do_doc for details
"""
import re
import time
import os

paramdir = "Param"

def build_param(file):
    """builds the parameter file for the NPK ProcessXX files
    """
    # open files
    print "Default parameters for:",file
    fin=open(file,'r')
    # read-in python file
    f=fin.read()
    lines = f.split("\n")

    if file != 'Interface.py':
        #then process each entries
        process_entries(lines)

def copy_pre(fout,lines):
    """ Process a comment block separated by the triple quote
    """
    l=lines.pop(0)
    while (not re.search('"""',l)):
        l=lines.pop(0)
    l="#  "+lines.pop(0)
    block=[]
    while (not re.search('"""',l)):
        
        block.append(l+"\n")
        l="#  "+lines.pop(0)
    fout.writelines(block)

def process_entries(lines):
    """ Process all entry definitions
    """
    while lines:
        l=lines.pop(0)
        func = re.findall('^def\s*(\w*)\((.*)\):',l)     # check if new entry found
        if func:     # if new entry found
            (title,arg)=func[0]            
            # get entry
            entry=[]
            while lines:
                l=lines.pop(0)
                if re.match('^def (\w*)',l):
                    lines.insert(0,l)
                    break
                else:
                    entry.append(l)
            process_entry(title,entry)


def process_entry(title,entry):
    """ process one entry
    """
    # get each action
    fout=open( os.path.join(paramdir, title + ".gtb"),"w")
    fout.writelines('# Default parameter file for '+title+'\n# created by do_default.py\n')
    fout.writelines('\n############################################################\n')
    copy_pre(fout,entry)   # copy first block
    fout.writelines('############################################################\n\n')
    while entry:
        l=entry.pop(0)
        t = re.findall('^\s*#\s*%action%\s*(.*)$',l)  # search action
        if t:
            action=t[0]
            param=[]
            while entry:
                l=entry.pop(0)
                s = re.findall('^\s*#\s*(.*)$',l)  # get text
                if s:
                    param.append(s[0])
                else:
                    break
            process_action(fout,action,param)
    fout.close()

def process_action(fout,action,param):
    fout.writelines('\n'+'#'*30 +'\n')
    fout.writelines('#  '+ action+ ' '*(26-len(action)) + '#\n')
    fout.writelines('#'*30 +'\n')
    while param:
        l=param.pop(0)
#        t = re.findall('^\s*#\s*%param%\s*(.*)\sdefault\s*(.w)\s*$',l)  # search defaut param
        fout.writelines("# "+l+"\n")
        t1 = re.findall('%param%\s+(\S+)\s+.*default.*"(.*)"',l)  # search defaut param        "string"
        t2 = re.findall('%param%\s+(\S+)\s+.*default.*\s(\S+)\s*$',l)  # search defaut param    value
        if t1:
#            print "T1",t1[0][0]
            fout.writelines('\n%s="%s"\n\n' % (t1[0]))
        else:
            if t2:
#                print "T2",t2[0][0]
                fout.writelines("\n%s=%s\n\n" % (t2[0]))

# Now do the work
build_param("Process1D.py")
build_param("Process2D.py")
build_param("Process3D.py")
build_param("ProcessDosy.py")
# remove dumb entries
print "cleaning"
for i in ("Dosy2D","FT1D","FT2D","FT_F1_2D","FT_F2_2D","MaxEnt1D","MaxEnt2D","PreDosy2D","write_file_1d","write_file_2d"):
    os.unlink(os.path.join(paramdir,i+".gtb"))
print "done"

