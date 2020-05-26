import os
from Environment import Environment

class LoginCommand:
    def login(self, environment):
        os.system('oc login %s' % environment.url)
        os.system('oc project %s' % environment.namespace)
    
    def logout(self):
        os.system('oc logout')