"""Types and type aliases used within the pyansiescapes package.

Types declared here:
    - **Colorbins**: a list of int
    - **ColorValueTuple**: integer tuple of size 3 (for rgb, hsl values)
    - **ColorValueList**: list of int (should be of size 3 for rgb hsl)
    - **ColorValue**: accept either ColorValueTuple or ColorValueList
    - **ColorArg**: all types accepted by :func:`.color`
        - int --> color id (e.g. 12)
        - str --> color id as str ("12"), name ("blue"), hexa ("#0000ff)
        - Colors --> obj of type :class:`.Colors`
        - Colors256 --> obj of type :class:`.Colors256`
        - ColorValue --> see **ColorValue**
    
    - **ColorArgTuple**: Tuple[int, ColorArg] used internally for parsing:
        - int: any in range(5)
            - 0 --> color argument is color id (e.g. 12 or "12")
            - 1 --> color argument is name (e.g. "blue")
            - 2 --> color argument is hexa (e.g. "#0000ff)
            - 3 --> color argument is rgb-value (e.g. (0, 0, 255))
            - 4 --> color argument is hsl-value (e.g. (240, 100, 50))
    
    - **ColorEnum**: either :class:`.Colors` or :class:`.Colors256`
    - **DrawingLevelArg**: type for *drawing_level* arg in :func:`._color`
        - int --> e.g. 3
        - bool --> e.g. False/0
        - str --> "foreground"
        - ColorDrawingLevel --> see :class:`.ColorDrawingLevel`
"""
from typing import List, Dict, Tuple, Callable, Any, Optional, Iterator, Union
from pyansiescapes.enums import *

ColorBins = List[int]
ColorValueTuple = Tuple[int, int, int]
ColorValueList = List[int]
ColorValue = Union[ColorValueTuple, ColorValueList]
ColorArg = Union[int, Colors, Colors256, str, ColorValue]
ColorArgTuple = Tuple[int, ColorArg]
ColorEnum = Union[Colors, Colors256]
DrawingLevelArg = Union[int, bool, str, ColorDrawingLevel]
