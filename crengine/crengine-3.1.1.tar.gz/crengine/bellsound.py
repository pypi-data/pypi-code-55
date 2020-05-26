######################################################################
### Change Ringing Engine
### Copyright (c) 2020 Jonathan Wilson
### Please refer to help/licence.txt for further information
### File: bellsound.py
### Description: Base "tower" class
### Last Modified: 24 May 2020
######################################################################


### import modules

from . import ringing
import os.path
from time import sleep


### soundinit - load sound module

def soundinit(interface):

    # nssound (Mac OS X)
    if interface in ['nssound']:
        import AppKit
        spkg=AppKit

    # pygame (UNIX)
    elif interface in ['pygame']:
        import pygame
        spkg=pygame
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=2048)
        pygame.mixer.get_init()

    # playsound (Windows/Mac)
    elif interface in ['playsound']:
        import playsound
        spkg=playsound

    # winsound (MS-Windows)
    elif interface in ['winsound']:
        import winsound
        spkg=winsound

    # other
    else:
        spkg=None

    # return package id
    return spkg



### Tower - base tower class

class Tower(ringing.RingObj):

    ### init - initialisation

    def __init__(self,name,nbells,bellset,sampledir):

        # initialise parent object
        ringing.RingObj.__init__(self,'tower',name,nbells)

        # initialise other attributes
        self.spkg=None
        self.interface='none'
        self.sampledir=sampledir
        self.description=''
        self.bellset=bellset
        self.bellmaps={}
        self.bellfiles={}
        self.bellsounds={}
        self.cover=True
        self.handstroke=False
        self.openlead=True
        self.gap=1.0
        self.missing=''

        # create bell maps - may be overriden
        for n in range(ringing.nbells_min,self.nbells+1):
            if n not in self.bellmaps.keys():
                self.bellmaps[n]=self.bellset[-n:]

        # set bell files
        for b in self.bellset:
            bellfile=os.path.join(self.sampledir,'%s.wav' %b)
            self.bellfiles[b]=bellfile

        # identify missing bell files
        for b in self.bellset:
            if not(os.path.isfile(bellfile)):
                self.missing+=b

    ### show

    def show(self):

        maps='\n'.join(
            ['%d : %s' %(n,self.bellmaps[n])
             for n in sorted(self.bellmaps.keys())])

        files='\n'.join(
            ['%s : %s' %(b,self.bellfiles[b])
             for b in sorted(self.bellfiles.keys())])

        s='''\
Bell Set        : %s
Interface       : %s

Maps:
%s

Samples:
%s
''' % (self.bellset, self.interface, maps, files)

        return self.showattribs()+s+'\n\n'+self.showvars()

    ### copy - doesn't actually copy but returns object reference

    def copy(self):
        return self

    ### setbellsounds - set bell sounds

    def setbellsounds(self,spkg):

        # Get reference to package
        self.spkg=spkg

        # none - sound off
        if spkg is None:
            self.interface='none'

        # nssound (AppKit) - Mac OS X
        # preload sound samples
        elif spkg.__name__.startswith('AppKit'):
            self.interface='nssound'
            for b in self.bellset:
                self.bellsounds[b]=spkg.NSSound.alloc()
                self.bellsounds[b].initWithContentsOfFile_byReference_(self.bellfiles[b],True)

        # pygame - Unix
        # preload sound samples
        elif spkg.__name__.startswith('pygame'):
            self.interface='pygame'
            for b in self.bellset:
                self.bellsounds[b]=spkg.mixer.Sound(self.bellfiles[b])

        # playsound - Windows/Mac
        # preloading not supported
        elif spkg.__name__.startswith('playsound'):
            self.interface='playsound'

        # winsound - Windows
        # preloading not supported
        elif spkg.__name__.startswith('winsound'):
            self.interface='winsound'

        # unknown
        else:
            self.interface='unknown'




    ### blockcheck - check compatibility of a block

    def blockcheck(self,block):
        return block.nbells+int(self.cover) in self.bellmaps.keys()

    ### set - set attributes for ringing

    def set(self,gap,cover,openlead,handstroke):
        self.gap=gap
        self.cover=cover
        self.openlead=openlead
        self.handstroke=handstroke

    ### nostrike - ring a row silently

    def nostrike(self,row):

        # gap at handstroke lead
        if self.openlead and self.handstroke:
            sleep(self.gap)

        # strike the row
        sleep(self.gap*row.nbells)

        # strike the cover bell
        if self.cover:
            sleep(self.gap)

        # change stroke
        self.handstroke=not(self.handstroke)

    ### chime (dummy)

    def chime(self,bells,gap):
        
        # nssound
        if self.interface in ['nssound']:
            for b in bells.upper():
                if b in self.bellset:
                    self.bellsounds[b].stop()
                    self.bellsounds[b].play()
                sleep(gap)

        # pygame
        elif self.interface in ['pygame']:
            for b in bells:
                if b in self.bellset:
                    self.bellsounds[b].stop()
                    self.bellsounds[b].play()
                sleep(gap)

        # playsound
        elif self.interface in ['playsound']:
            for b in bells.upper():
                if b in self.bellset:
                    self.spkg.playsound(self.bellfiles[b],False)
                sleep(gap)

        # winsound
        elif self.interface in ['winsound']:
            for b in bells.upper():
                if b in self.bellset:
                    self.spkg.PlaySound(self.bellfiles[b],self.spkg.SND_FILENAME|self.spkg.SND_ASYNC)
                sleep(gap)

        # silent
        else:
            for b in bells.upper():
                sleep(gap)


    ### rowstrike - strike a row of a method

    def rowstrike(self,row):

        # map
        bellmap=self.bellmaps[row.nbells+int(self.cover)]

        # add gap at handstroke lead
        if self.openlead and self.handstroke:
            sleep(self.gap)

        # nssound
        if self.interface in ['nssound']:

            for n in range(1,row.nbells+1):
                b=bellmap[row.places[n]-1]
                self.bellsounds[b].stop()
                self.bellsounds[b].play()
                sleep(self.gap)

            if self.cover:
                b=bellmap[row.nbells]
                self.bellsounds[b].stop()
                self.bellsounds[b].play()
                sleep(self.gap)

        # pygame
        elif self.interface in ['pygame']:

            for n in range(1,row.nbells+1):
                b=bellmap[row.places[n]-1]
                self.bellsounds[b].stop()
                self.bellsounds[b].play()
                sleep(self.gap)

            if self.cover:
                b=bellmap[row.nbells]
                self.bellsounds[b].stop()
                self.bellsounds[b].play()
                sleep(self.gap)

        # playsound
        elif self.interface in ['playsound']:

            for n in range(1,row.nbells+1):
                b=bellmap[row.places[n]-1]
                self.spkg.playsound(self.bellfiles[b],False)
                sleep(self.gap)

            if self.cover:
                b=bellmap[row.nbells]
                self.spkg.playsound(self.bellfiles[b],False)
                sleep(self.gap)

        # winsound
        elif self.interface in ['winsound']:

            for n in range(1,row.nbells+1):
                b=bellmap[row.places[n]-1]
                self.spkg.PlaySound(self.bellfiles[b],SND_FILENAME|SND_ASYNC)
                sleep(self.gap)

            if self.cover:
                b=bellmap[row.nbells]
                self.spkg.PlaySound(self.bellfiles[b],self.spkg.SND_FILENAME|self.spkg.SND_ASYNC)
                sleep(self.gap)

        # otherwise silent...
        else:

            sleep(self.gap*row.nbells)
            if self.cover:
                sleep(self.gap)

        # change stroke
        self.handstroke=not(self.handstroke)


    ### stopstrike - stop all bells sounding

    def stopstrike(self):

        # nssound
        if self.interface in ['nssound']:
            for b in self.bellset:
                self.bellsounds[b].stop()

        # pygame
        elif self.interface in ['pygame']:
            for b in self.bellset:
                self.bellsounds[b].stop()

        # playsound
        elif self.interface in ['playsound']:
            pass

        # winsound
        elif self.interface in ['winsound']:
            pass

        # silent
        else:
            pass





