"""
GMLP.game
=========
"""
from __future__ import absolute_import

import os

import pygame
from pygame.locals import QUIT


class Setup:
    """
    GMLP 0.2 Setup. With Setup there are a few keywords that go with Setup.
    \nTo print the keywords type ``print(Setup.keywords)`` and it will print the keywords.
    """
    keywords = ['height', 'width', 'bg', 'name', 'objects']
    def __init__(self, **settings):
        for i in settings:
            if 'name' in settings:
                self.name = settings["name"]
            else:
                self.name = 'Window'

            if 'bg' in settings:
                self.bg = settings['bg']
            else:
                self.bg = (0, 0, 0)
            
            if 'height' in settings:
                self.h = settings['height']
            else:
                self.h = 0
            
            if 'width' in settings:
                self.w = settings['width']
            else:
                self.w = 0

            if 'objects' in settings:
                self.objects = settings['objects']
            else:
                self.objects = None
        
        self.gameDisplay = pygame.display.set_mode((self.h, self.w))
    
    def ImageView(self, image_dir, x, y, **kwargs):
        self.img = pygame.image.load(image_dir)
        self.x = x
        self.y = y
        for i in kwargs:
            if 'size' in kwargs:
                self.size = kwargs['size']
                self.img = pygame.transform.scale(self.img, self.size)
            else:
                self.size = None
        

    def View(self):
        
        pygame.init()
        pygame.display.set_caption(self.name)

        self.closed = False
        while not self.closed:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.closed = True

            self.gameDisplay.fill(self.bg)
            try:
                if self.ImageView.__call__:
                    self.gameDisplay.blit(self.img, (self.x, self.y))
            except Exception:
                pass
            pygame.display.update()
        pygame.quit()

game = Setup(
    name="MyWindow",
    bg=(255, 255, 255),
    height=500,
    width=500,
    objects=[
        'C:/Users/DrewM/Downloads/snek2.jpg'
    ]
)