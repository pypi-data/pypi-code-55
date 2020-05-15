"""
Hello and welcome to DrawPy!
This is a simple graphics package for python based on pygame, so you need pygame to run this.
This package is meant for graphics and basic games and GUI's.
Here is a little example to get you started. For more, run example_drawing() or example_animation():
__________________________________________________________
from DrawPy import *


def main():
    screen = Window((500, 500), "MyWindow")  # Creates the window
    screen.circle([250, 250], 250)  # Draws a circle centered at (250, 250) with a radius of 250
    draw()  # Flips the drawings on to the screen
    done()  # Waits to close the window


main()
-----------------------------------------------------------
run the help() function for more help
Please Enjoy!
"""
has_pygame = True
try:
    import pygame

except:
    print("You need pygame to run this")
    has_pygame = False
assert has_pygame == True

pygame.init()
# Defining some variables and functions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

PI = 3.141592653

quit = pygame.quit

QUIT = pygame.QUIT
MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
MOUSEBUTTONUP = pygame.MOUSEBUTTONUP
KEYDOWN = pygame.KEYDOWN
KEYUP = pygame.KEYUP

draw = pygame.display.flip

clock = pygame.time.Clock


# Functions
def done():
    """
    Stops and waits for the user to click the exit button
    :param events: The events
    :return: None
    """

    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False


def stop():
    """
    DO NOT USE!
    :return: none
    """
    while True:
        pass


def kind(event):
    """
    Finds the type of an event
    :param event: the event
    :return: the type of the event
    """
    return event.type


def get_mouse():
    """
    Gets the location of the mouse
    :return: the location of the mouse
    """
    return pygame.mouse.get_pos()


def check_quit():
    """
    Checks if the user has quit
    :return: True if the user has quit, otherwise returns False
    """
    if pygame.QUIT in [event.type for event in pygame.event.get()]:
        return True
    return False


def frame_rate(num=60):
    """
    Sets a frame rate
    :param num: the frame_rate
    :return: None
    """
    clock = pygame.time.Clock()
    clock.tick(num)


def get_events():
    return [event.type for event in pygame.event.get()]


def wait(seconds):
    """Stops the program for a certain amount of seconds"""
    pygame.time.delay(seconds * 1000)


class Window:
    """Creates a window"""
    DEFAULT = "default"

    def __init__(self, size=(500, 700), caption="Untitled Window", color=WHITE):
        self.size = size
        self.caption = caption
        self.color = color
        self.handlers = {}
        self.key_log = []
        self.win = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)
        self.win.fill(self.color)
        draw()

    def rectangle(self, rect, color=BLACK, thickness=1):
        """Draws a rectangle"""
        if rect is None:
            rect = [0, 0, 0, 0]
        pygame.draw.rect(self.win, color, rect, thickness)

    def circle(self, circle, radius, color=BLACK, thickness=1):
        """Draws a circle"""
        if circle is None:
            circle = [0, 0]
        pygame.draw.circle(self.win, color, circle, radius, thickness)

    def line(self, line, color=BLACK, thickness=1):
        """Draws a line"""
        if line is None:
            line = [0, 0, 0, 0]
        pygame.draw.line(self.win, color, line[:2], line[2:], thickness)

    def ellipse(self, ellipse, color=BLACK, thickness=1):
        """Draws an ellipse"""
        if ellipse is None:
            ellipse = [0, 0, 0, 0]
        pygame.draw.ellipse(self.win, color, ellipse, thickness)

    def arc(self, arc, start_angle, stop_angle, color=BLACK, thickness=1):
        """Draws an arc"""
        if arc is None:
            arc = [0, 0, 0, 0]
        pygame.draw.arc(self.win, color, arc, start_angle, stop_angle, thickness)

    def clear(self):
        """Clears the screen to its original color"""
        self.win.fill(self.color)

    def register(self, kind, func):
        """Registers a function to handle a certain kind of event"""
        if kind not in self.handlers:
            self.handlers[kind] = []
        self.handlers[kind].append(func)

    def go(self, framerate=60, clear=False):
        """Runs the program and acts upon the events"""
        while True:
            if Window.DEFAULT in self.handlers:
                for func in self.handlers[Window.DEFAULT]:
                    func()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
                if event.type in self.handlers:
                    for func in self.handlers[event.type]:
                        func(event)
            pygame.display.flip()
            clock = pygame.time.Clock()
            clock.tick(framerate)
            if clear:
                self.clear()


# Examples

def example_drawing():
    """Draws a circle in the middle of a screen"""
    screen = Window((500, 500), "MyWindow")  # Creates the window
    screen.circle(BLACK, [250, 250], 250, 0)  # Draws a circle centered at (250, 250) with a radius of 250

    draw()  # Flips the circle to the screen

    done()  # Waits to close the window


def example_animation():
    """Animates a circle moving around a screen"""
    screen = Window(caption="Moving circle")  # Creates the window

    # Set the speed of the circle
    x_change = 5
    y_change = 5
    # Set the initial position of the circle
    x_pos = 50
    y_pos = 50

    # Main loop, used for animations and some games
    while not check_quit():  # Loop until the user closes the window
        screen.circle( [x_pos, y_pos], 25)  # Draws the circle
        x_pos += x_change  # Moves the position of the circle
        y_pos += y_change
        # Causes the circle to bounce if it touches the edge
        if x_pos >= 475:
            x_change = -1 * abs(x_change)
        if x_pos <= 25:
            x_change = abs(x_change)
        if y_pos >= 675:
            y_change = -1 * abs(y_change)
        if y_pos <= 25:
            y_change = abs(y_change)
        draw()  # Flips the circle to the screen
        frame_rate(60)  # Sets a frame rate of 60 fps
        screen.clear()  # Clears the screen
    quit()  # Quits the program


def example_event():
    # Used mainly for games or animation that handle events.
    screen = Window((500, 700), "My Window", BLUE)  # Creates the screen

    def default():  # Sets the default function
        screen.ellipse([0, 0, 500, 700])

    def on_click(event):  # Sets an on click function
        screen.ellipse([0, 0, 500, 700], thickness=0)  # Draws a filled in ellipse

    screen.register(screen.DEFAULT, default)  # Registers the functions
    screen.register(MOUSEBUTTONDOWN, on_click)
    screen.go()


# A help function
def help():
    """A help function for the user"""
    description = """Hello and welcome to DrawPy help! Here are a list of commands: 

    screen = Window((100, 100), "MyWindow", BLUE)  # Creates a window with dimensions 100x100 

    Drawing Commands:
    Note that for the drawing commands below, the color and thickness arguments are optional
    screen.rectangle([0, 0, 50, 50], BLACK, thickness=1)  # Draws a black rectangle with a top left corner at (0, 0) and
        a length and width of 50 
    screen.circle([50, 50], 50, 1])  # Draws a red circle centered at (50, 50) with a radius of 50 
    screen.line([0, 0, 100, 100], WHITE)  # Draws a white line from (0, 0) to (100, 100)
    screen.ellipse([0, 0, 100, 100], 1)  # Draws an ellipse inside the rectangle given by the coordinates
        [0, 0, 100, 100]
    screen.arc([0, 0, 100, 100], PI/4, PI/2)  # Draws an arc of the ellipse above. Starts at angle PI/4 and
        stops at PI/2
    screen.clear()  # Clears the screen to it's original color

    Other helpful commands:
    check_quit()  # Checks if the user has pressed the close button
    done()  # Waits before closing
    quit()  # Quits the graphical part of the program
    frame_rate(60)  # Sets a frame rate of 60 fps
    events()  # Returns the event log
    get_mouse()  # Returns the position of the mouse

    There are three formats for using this package:

    format 1, for simple graphics and certain animations:

    screen = Window((500, 700), "My Window", RED)
    screen.circle(BLACK, [50, 50], 50, 1)  # This drawing will stay here forever
    draw()  # Draws it to the screen
    done()  # Waits for the user to quit the program

    format 2, for more complex graphics and animations:

    screen = Window((500, 700), "My Window", RED)
    while not check_quit():  # Runs until the user has quit the program
        screen.circle([50, 50], 50) 

        draw()  # Flips the drawing to the screen
        frame_rate(60)  # Sets a frame rate of 60 fps
        screen.clear  # Clears the screen
    quit()  # Quits the program

    format 3, more advanced, for event based graphics and games

    screen = Window((500, 700), "My Window", BLUE)  # Makes the screen


    def default():  # Will always run this function
        screen.ellipse([0, 0, 500, 700])


    def on_click(event):  # Makes a function that runs when the mouse is pressed
        screen.ellipse([0, 0, 500, 700], thickness=0)


    screen.register(screen.DEFAULT, default)  # Registers the functions
    screen.register(MOUSEBUTTONDOWN, on_click)
    screen.go())  # Runs the program
    """
    print(description)
