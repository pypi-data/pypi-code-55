#importing modules
from tkinter import *
from .storage import database
from PIL import Image, ImageTk
import re
import time

players = 0

#main class
class Game():
    def __init__(self, title, width=100, height=100, bg="lightblue"):
        self.screen = Tk()
        self.title = title
        self.bg = bg
        self.width = width
        self.height = height
        self.screen.title(title)
        self.screenType = "fixed"
        self.canvas = Canvas(self.screen, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill=self.bg)
        self.canvas.bind_all("<Key>", self.react_to_key)
        
        self.characters = []
        self.blocks = []
        
        self.gravity = 0
        self.running = False
    
    def title(self, screentitle):
        if screentitle:
            self.title = screentitle
            return self.screen.title(screentitle)
    
    def update(self):
        self.canvas.update()
    
    def add(self, object):
        if isinstance(object, Character):
            object.canvas = self.canvas
            self.characters.append(object)
        elif isinstance(object, Block):
            object.canvas = self.canvas
            self.blocks.append(object)
    
    def run(self):
        for character in self.characters:
            character.draw()
        for block in self.blocks:
            block.draw()
        self.running = True
        while self.running:
            for character in self.characters:
                character.move(0, character.movementY)
                #TODO: let character stop falling if it is standing on a block
                if not collideTopOfAnyOf(character.x, character.y, character.width, character.height, self.blocks):
                    character.movementY += self.gravity
            self.canvas.update()
            time.sleep(0.01)
    
    #when key is pressed
    def react_to_key(self, event):
        key = event.keysym
        if key == "Left":
            self.onkeyleft()
        elif key == "Right":
            self.onkeyright()
        elif key == "Up":
            self.onkeyup()
    
    #keybinds
    def onkeyleft(self):
        pass
    def onkeyright(self):
        pass
    def onkeyup(self):
        pass
    
    @classmethod
    def createCharacter(cls, src):
        return Character(src)
    
    #decorator
    def onkeypress(self, key):
        def bind(func):
            if key == "left":
                self.onkeyleft = func
            elif key == "right":
                self.onkeyright = func
            elif key == "up":
                self.onkeyup = func
            else:
                raise ModuleError("Python2d doesn't support the key: " + key)
            return func
        return bind

class Player(Character):
    def __init__(self, path, type="static"):
        if players == 0:
            super().__init__(path, type)
            players += 1
        else:
            raise ModuleError("You can only define one player.")

#character class
class Character():
    def __init__(self, path, type="static"):
        self.x = 0
        self.y = 0
        self.movementY = 0
        self.canvas = None
        if type == "static":
            if re.match(r".*\.(png|jpg)", path):
                self.path = path
                self.img = Image.open(self.path)
                self.width, self.height = self.img.size
                self.tatras = ImageTk.PhotoImage(self.img)
            else:
                raise ValueError(path + " is not an image.")
        
    
    def place(self, **kwargs):
        try:
            self.x = kwargs["x"]
        except KeyError:
            pass
        try:
            self.y = kwargs["y"]
        except KeyError:
            pass
    
    def move(self, moveX, moveY):
        if self.canvas:
            self.canvas.move(self.image, moveX, moveY)
    
    def draw(self):
        if self.canvas:
            self.image = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.tatras)
    
    #game methods
    def jump(self):
        self.movementY = -15

#block class
class Block():
    def __init__(self, **kwargs):
        try:
            self.color = kwargs["color"]
        except KeyError:
            self.color = "black"
        try:
            self.width = kwargs["width"]
        except KeyError:
            self.width = 100
        try:
            self.height = kwargs["height"]
        except KeyError:
            self.height = 100
        self.x = 0
        self.y = 0
        self.canvas = None
    
    def place(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def draw(self):
        if self.canvas:
            self.graph = self.canvas.create_rectangle(self.x, self.y, self.width, self.height, fill=self.color)

#collision function
def collide(x1, y1, length1, height1, x2, y2, length2, height2):
    collideX = (x1 > x2 and x1 < x2 + length2) or (x1 + length1 > x2 and x1 + length1 < x2 + length2) or (x1 < x2 and x1 + length1 > x2 + length2)
    collideY = (y1 > y2 and y1 < y2 + height2) or (y1 + height1 > y2 and y1 + height1 < y2 + height2) or (y1 < y2 and y1 + height1 > y2 + height2)
    return collideX and collideY

def collideTopOfAnyOf(x1, y1, length1, height1, arr):
    result = False
    for item in arr:
        result = result or collide(x1, y1, length1, height1, item.x, item.y, item.width, 10)
    return result
