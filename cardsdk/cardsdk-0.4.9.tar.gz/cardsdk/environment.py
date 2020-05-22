#-*-coding:utf-8-*-
#! /usr/bin/python3

import os,json
from .gui import *

class cardsdkEnv(object):
    def __init__(self):
        self.version = '0.0.1'
        cui=gui()
        self.i=cui.i
        self.s=cui.s
        self.w=cui.w
        self.c=color()

    def checkInstalled(self,command):
        commandPass=0
        for cmdpath in os.environ['PATH'].split(':'):
            if os.path.isdir(cmdpath) and command in os.listdir(cmdpath):
                commandPass=1
            if not commandPass:
                commandPass=0
        return commandPass

    def checkHomebrew(self):
        if not self.checkInstalled('brew'):
            self.i('start install HomeBrew .....')
            os.system('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"')
        else:
            self.s('brew existed')

    def checkNode(self):
        if not self.checkInstalled('node'):
            self.i('start install node .....')
            os.system('brew install node')
            os.system('npm install cnpm -g')
        else:
            self.s('node existed')
            self.i('start check cnpm')
            if not self.checkInstalled('cnpm'):
                os.system('npm install cnpm -g')
            else:
                self.i('cnpm is installed')


    def checkAccore(self):
        if not self.checkInstalled('accore1'):
            self.i('start install AntCardSDK Build tools .....')
            os.system("cnpm install @antcube/core-v1 -g")
        else:
            streamLocal = os.popen('npm ls @antcube/core-v1 -g -json')
            localInfo = json.loads(streamLocal.read())
            localVersion = localInfo["dependencies"]["@antcube/core-v1"]["version"]
            stream = os.popen('npm info @antcube/core-v1 -json')
            corev1Json = stream.read()
            corev1JsonObj = json.loads(corev1Json)
            latestVersion = corev1JsonObj["dist-tags"]["latest"]
            if latestVersion != localVersion:
                self.i('start upgrade AntCardSDK Build tools .....')
                opcmd = 'cnpm install' + ' @antcube/core-v1'+'@'+latestVersion +' -g'
                os.system(opcmd)
            else:
                pass
    def init(self):
        os.system('')
    
    def AntCardSDKSetup(self):
        self.checkHomebrew()
        self.checkNode()
        self.checkAccore()
