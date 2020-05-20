import os

if "ZLIBTUI_BROWSER" in os.environ:
    BROWSER = os.environ["ZLIBTUI_BROWSER"]
else:
    BROWSER = "firefox"


