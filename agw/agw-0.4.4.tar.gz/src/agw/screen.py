import pyautogui as ag
from pyscreeze import ImageNotFoundException


class Region:

    def __init__(self, x, y, x1=None, y1=None, w=None, h=None):
        self.x = x
        self.y = y

        if x1 and y1 and not w and not h:
            self.x1 = x1
            self.y1 = y1
            self.w = x1 - x
            self.h = y1 - y
        elif w and h and not x1 and not y1:
            self.w = w
            self.h = h
            self.x1 = x + w
            self.y1 = y + h
        else:
            raise Exception("Either supply x1 and y1 coordinates, or the width and high values. Not both")

    @property
    def box(self):
        return (self.x, self.y, self.w, self.h)

    @staticmethod
    def from_coordinates(x, y, x1, y1):
        return Region(x, y, x1=x1, y1=y1)

    @staticmethod
    def from_measurements(x, y, w, h):
        return Region(x, y, w=w, h=h)



def locate_image(image, region=None):
    try:
        if isinstance(region, Region):
            region = region.box
        return ag.locateOnScreen(image, region=region)
    except ImageNotFoundException:
        return None


def image_located(image, region=None, note=None, action=None):

    result = locate_image(image, region=region)

    if result and note:
        print(note)

    if result and action:
        action()

    return result
