# +-------------------------------------------------------------------------------+
#
#      Program:    setup.py
#
#      Purpose:    setup for remote open control - key enabling technology (Rocket)
#
#      Target:     ARMV61A
#
#      Author:     Martin Shishkov
#
#      License:    GPL 3
# +-------------------------------------------------------------------------------+
import os

class Init:
    def __init__(self):
        print('Installing rocket-pi')
        
    def get_package(self):
        linkPyPi = "https://files.pythonhosted.org/packages/74/d7/d0eafbaec45f24c2a9a23627f3c6fc2ceef239412a1e2dc50a03e4d9b765/rocket-pi-1.0a1.tar.gz"
        rocket = "rocket-pi-1.0a1"
        if not os.path.isdir(rocket):
            print('downloading rocket-pi')
            os.system("wget " + linkPyPi)
            os.system(("tar xvzf %s.tar.gz" % (rocket)))
            os.chdir(rocket)
            os.system("sudo python3 setup.py bdist")
            
            
            
 
 
 
i = Init()
i.get_package()    