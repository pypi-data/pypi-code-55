#  Copyright (c) 2020 Netflix.
#  All rights reserved.

# Implementation libs
from kaiju_automator_lib.__version__ import __version__
from netflix_update_notify import UpdateNotifier

UpdateNotifier.notify_of_updates("kaiju-automator-lib", __version__)
