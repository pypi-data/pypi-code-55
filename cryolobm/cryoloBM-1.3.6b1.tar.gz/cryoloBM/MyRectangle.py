from matplotlib.patches import Rectangle


class MyRectangle:
    def __init__(self, xy, width, height, angle=0.0, est_size=None, **kwargs):
        self.confidence = None
        self.est_size = est_size
        self.xy = xy
        self.width = width
        self.height = height
        self.angle = angle
        self.rectInstance = None
        self.kwargs = kwargs
        #super(MyRectangle, self).__init__()

    def getRect(self):
        if self.rectInstance == None:
            self.rectInstance = Rectangle(self.xy, self.width, self.height, self.angle, **self.kwargs)
        return self.rectInstance

    def set_confidence(self,confidence):
        self.confidence = confidence
