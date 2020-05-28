class Container:
    """
    Example:
    keys = ['x','y']
    values = [1,2]
    a,b = Container(keys),Container(keys,values)
    a.x,a.y >>> None, None
    b.x,b.y >>> 1, 2
    -----------
    keys = list of names to be set as attribute names
    values = list of values parallel to keys to be set as values
    """
    def __init__(self,keys,values=None):
        import numpy as np
        if not values:
            values = []
            for i in keys:
                values.append(None)
        for i,ii in enumerate(keys):
            setattr(self, ii, values[i])