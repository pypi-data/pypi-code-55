#from Jupytils.jcommon import *

def LoadJupytils(abspath=None, debug=False):
    ip = get_ipython()
    if(abspath is None):
        abspath =os.path.dirname(Jupytils.__file__)
    if(debug):
        print("loading jupytils ... from: "+abspath);
        
    #ip.run_line_magic(magic_name="run", line=abspath+"/DBUtils.py")
    #c = readFile(abspath+"/ajax.html")
    #display(HTML(c))

    
try:
    #LoadJupytils()
	pass
except:
    pass
