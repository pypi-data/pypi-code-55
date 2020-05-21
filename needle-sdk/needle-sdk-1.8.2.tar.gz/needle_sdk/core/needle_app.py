from .classes import NeedleApp
from .wrappers import init_wrapper_store
import threading


def init_app(flask_app=None, debug=False, show_blocked_message=False, adv_debug=False, sdk_version=''):
    global needle_app
    needle_app = NeedleApp(debug=debug, show_blocked_message=show_blocked_message, flask_app=flask_app)
    needle_app.agent_version = sdk_version
    needle_app.adv_debug = adv_debug

    if not needle_app.run_agent:
        print('Needle.sh: Stopping agent.')
        return

    # Initialise wrappers
    init_wrapper_store()

    try:
        # Start thread to send data to Needle.sh server
        x = threading.Thread(target=needle_app.api_thread, args=(), daemon=True)
        x.start()
    except Exception as e:
        error_data = str(e)
        needle_app.add_error('Error starting Needle.sh thread to send data', error_data)

    return needle_app


def get_needle_app():
    global needle_app
    return needle_app


needle_app = None