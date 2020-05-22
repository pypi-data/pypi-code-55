from .output import *
from .collection import *
from .tags import *

try:
    disable_scroll('.output_scroll_disabled .output_scroll')
except Exception as e:
    print("Couldn't add disabled output scroll styles: ({}) {}".format(type(e), e))
