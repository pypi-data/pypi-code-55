# Copyright (c) 2020, Varlogix Technologies
# All rights reserved.
# Our terms: https://needle.sh/terms

from .core.needle_app import init_app


# Start Needle.sh
def start(flask_app=None, debug=False, show_blocked_message=False, adv_debug=False):
    print("Needle.sh: Starting SDK (version " + sdk_version + ")")

    init_app(debug=debug, show_blocked_message=show_blocked_message, adv_debug=adv_debug, flask_app=flask_app,
             sdk_version=sdk_version)


# SDK version
sdk_version = '1.8.2'
