#!/usr/bin/env python
 
"""
pyplayground.py
 
Platform for simple games
 
URL:     https://github.com
Author:  Mychajlo Chodorev
License: Do What The Fuck You Want To Public License (WTFPL)
         See http://www.wtfpl.net/
"""
 
####
import math
import numpy as np
import os
import pygame as pyg
import threading

class Game(object):
    __actors = {}
    __width = None
    __height = None
    __screen = None
    __background = None
    __instance = None
    __instance_created = False
    
    should_stop = False
    '''
    When set to True all thread are stopped
    '''

    def __init__(self, size=(0, 0), caption='', debug=False):
        '''
        size - tuple of width and height of the game window
        caption - caption of the game window
        debug - set to True to run debug mode (like showing rectangles of the actors)
        '''
        if not self.__instance_created:
            self.__debug = debug
            self.__width = size[0]
            self.__height = size[1]
            self.__screen = pyg.display.set_mode(size, pyg.DOUBLEBUF | pyg.HWSURFACE)
            pyg.display.set_caption(caption)
            pyg.key.set_repeat(10, 10)
            self.__background = pyg.Surface(self.__screen.get_size()).convert()
            self.__background.fill((0, 0, 0))
            self.__instance_created = True

    def __new__(cls, size=None, caption=None, debug=False):
        if Game.__instance is None:
            Game.__instance = object.__new__(cls)
        return Game.__instance
        
    def __run_event_handler(self, actors, handler, *vargs):
        '''
        Runs event handler for all actors in the list 
        If there are additional arguments provided they are passed to the handler
        '''
        for actor in actors:
            if isinstance(actor, Actor):
                try:
                    if len(vargs):
                        getattr(actor, handler)(*vargs)
                    else:
                        getattr(actor, handler)()
                except AttributeError as e:
                    #print(e)
                    pass
                    
    def add_actor(self, actor):
        '''
        Adds actor to the list
        '''
        self.__actors[actor.name] = actor
        
    def get_actor(self, actor_name):
        '''
        Returns actor object by its name
        '''
        return self.__actors[actor_name]

    def calc_rad_alphas(radius, n):
        """
        Calculate linear radius and alpha values
        """
        assert 0 < n < 256, "Invalid number of holes!"

        rad_step = radius // n
        alpha_step = 256 // n
        self.__rad_alphas = [(radius - i * rad_step, 255 - i*alpha_step) for i in range(n)]


    def calc_centers(self, center, pos, holes):
        """
        Calculate center points from center (of window) to mouse position
        """

        cx, cy = center
        mx, my = pos
        vx, vy = mx - cx, my - cy

        xs = vx // holes
        ys = vy // holes
        self.centers = [(cx + xs*i, cy + ys*i) for i in range(holes)]

    def rename_actor(self, actor):
        '''
        Replaces actor entry with another one of new actor name
        '''
        for key, value in self.__actors.items():
            if value == actor:
                self.__actors.pop(key)
                self.add_actor(actor)
                break

    def run(self, *opts):
        """
        Mainloop
        """
        
        ######## Run on_start event handlers #####################
        self.__run_event_handler(opts, 'on_start')
            
        mainloop = True
        while mainloop:
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    mainloop = False
                elif event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_ESCAPE:
                        mainloop = False
                    else:
                        self.__run_event_handler(opts, 'on_key_down', event.key)
                elif event.type == pyg.KEYUP:
                    self.__run_event_handler(opts, 'on_key_up', event.key)

            self.show(opts)
        self.should_stop = True
        pyg.quit()        

    def show(self, actors):
        """
        Draw all
        """
        self.__screen.blit(self.__background, (0, 0))
        for actor in actors:
            if actor.is_visible:
                if actor.get_skin().get_locked():
                    actor.get_skin().unlock()
                try:
                    self.__screen.blit(actor.get_skin(), actor.get_position())
                except Exception as e:
                    print(actor)
                    print(actor.get_skin().get_locked())
                    print(e)
                #### Draw rectangle around objects for debugging ############
                if self.__debug:
                    rect = actor.get_skin().get_rect(topleft=actor.get_position())
                    pyg.draw.rect(self.__screen, (255,0,0), rect, 2)
        pyg.display.flip()
        
class Actor(object):
    __original_skin = None
    __image = None
    __visible = False
    __x = 320
    __y = 240
    __original_heading = 0
    __heading = 0
    
    name = None
    
    def __new__(cls):
        this = object.__new__(cls)
        this.name = cls.__name__
        Game().add_actor(this)
        return this
    
    def hide(self):
        '''
        Hides actor
        '''
        self.__visible = False
        
    def get_position(self):
        '''
        Returns tuple of X and Y of the actor
        '''
        return (self.__x, self.__y)
      
    def get_skin(self):
        '''
        Returns Surface object of the actor
        '''
        return self.__image
      
    @property
    def is_visible(self):
        '''
        Returns True if actor is visible and False otherwise
        '''
        return self.__visible
        
    def move(self, distance):
        '''
        Move actor along the heading.
        Move forward if distance is posititive and backwards if it's negative
        '''
        dx = distance * math.cos(math.pi / 180 * self.__heading)
        dy = distance * math.sin(math.pi / 180 * self.__heading)
        self.__x += dx  
        self.__y += dy
        
    def run_forever(self, method):
        '''
        Runs provided method endlessly in separate thread until Game.should_stop is positive
        '''
        def worker(method):
            try:
                while not Game.should_stop:
                    method()
            except AttributeError:
                pass
        threading.Thread(target=worker, args=(method,)).start()     
    
    def turn(self, angle):
        '''
        Rotate actor angle degrees counter clockwise if angle is positive
        and clockwise if it's negative
        '''
        self.__heading += angle
        (x0, y0) = self.__image.get_size()
        self.__image = pyg.transform.rotate(self.__original_image, self.__original_heading - self.__heading)
        (x1, y1) = self.__image.get_size()
        dx = x1 - x0
        dy = y1 - y0
        self.__x -= dx % 2
        self.__y -= dy % 2
        
    def strife(self, distance):
        '''
        Move actor perpendicular to its heading.
        Move right to heading if distance is positive
        and left to heading if it's negative
        '''
        dx = distance * math.cos(math.pi / 180 * (self.__heading + 90))
        dy = distance * math.sin(math.pi / 180 * (self.__heading + 90))
        self.__x += dx  
        self.__y += dy
            
    def set_heading(self, heading):
        '''
        Set initial heading of the actor. 
        '''
        self.__heading = self.__original_heading = heading
        
    def set_name(self, name):
        '''
        Set the name of the actor. Default actor's name is its class name
        '''
        self.__name = name
        Game().rename_actor(self)
        
    def set_position(self, x, y):
        '''
        Moves actor to the provided coordinates
        '''
        self.__x = x
        self.__y = y
        
    def set_skin(self, image_path):
        '''
        Sets skin of the actor to provided image file
        '''
        pic = pyg.image.load(image_path)
        if pic.get_alpha():
            self.__image = pic.convert_alpha()
        else:
            self.__image = pic.convert()
        self.__original_image = self.__image
            
    def show(self):
        '''
        Shows actor
        '''
        self.__visible = True
      
    def touches_actor(self, actor_name):
        '''
        Returns True if actor touches provided one.
        Checks actor's skins touching rather than rectangles
        '''
        actor = Game().get_actor(actor_name)
        r1 = self.__image.get_rect(topleft=(self.__x, self.__y))
        r2 = actor.__image.get_rect(topleft=actor.get_position())
        result = False
        if r1.colliderect(r2):
            intersection = r1.clip(r2)
            # print(intersection)
            # print(intersection.y - r1.y, intersection.y - r1.y + intersection.h, intersection.x - r1.x, intersection.x - r1.x + intersection.w)
            r1pixels = pyg.surfarray.array2d(self.__image).transpose()
            r1p_x = r1pixels[
                        intersection.y - r1.y:intersection.y - r1.y + intersection.h, 
                        intersection.x - r1.x:intersection.x - r1.x + intersection.w
                    ]        
            # print("R1", r1p_x)
            # print("R1 sum", r1p_x.sum())
            if r1p_x.sum() != 0:
                r2pixels = pyg.surfarray.array2d(actor.get_skin()).transpose()
                r2p_x = r2pixels[
                            intersection.y - r2.y:intersection.y - r2.y + intersection.h, 
                            intersection.x - r2.x:intersection.x - r2.x + intersection.w
                        ]
                # print("R2", r2p_x)
                # print("R2 sum", r2p_x.sum())
                # print(np.multiply(r1p_x, r2p_x))
                result = np.multiply(r1p_x, r2p_x).sum() != 0
                del r2p_x
            del r1p_x
        return result
        
    def touches_edge(self):
        '''
        Returns True if actor touches any edge
        '''
        current_surface_size = pyg.display.get_surface().get_size()
        my_size = self.__image.get_size()
        return (
            self.__x <= 0 or 
            self.__x + my_size[0] >= current_surface_size[0] or
            self.__y <= 0 or
            self.__y + my_size[1] >= current_surface_size[1]
        )