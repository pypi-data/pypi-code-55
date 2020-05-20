# Taken from https://github.com/click-contrib/click-spinner
# Modifying pipe to output to stderr, as completion is based on reading from stdout

import sys
import threading
import time
import itertools


class Spinner(object):
    spinner_cycle = itertools.cycle(["-", "/", "|", "\\"])

    def __init__(self, beep=False, disable=False, force=False):
        self.disable = disable
        self.beep = beep
        self.force = force
        self.stop_running = None
        self.spin_thread = None

    def start(self):
        if self.disable:
            return
        if sys.stderr.isatty() or self.force:
            self.stop_running = threading.Event()
            self.spin_thread = threading.Thread(target=self.init_spin)
            self.spin_thread.start()

    def stop(self):
        if self.spin_thread:
            self.stop_running.set()
            self.spin_thread.join()

    def init_spin(self):
        while not self.stop_running.is_set():
            sys.stderr.write(next(self.spinner_cycle))
            sys.stderr.flush()
            time.sleep(0.25)
            sys.stderr.write("\b")
            sys.stderr.flush()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.disable:
            return False
        self.stop()
        if self.beep:
            sys.stderr.write("\7")
            sys.stderr.flush()
        return False


def spinner(beep=False, disable=False, force=False):
    """This function creates a context manager that is used to display a
    spinner on stdout as long as the context has not exited.
    The spinner is created only if stdout is not redirected, or if the spinner
    is forced using the `force` parameter.
    Parameters
    ----------
    beep : bool
        Beep when spinner finishes.
    disable : bool
        Hide spinner.
    force : bool
        Force creation of spinner even when stdout is redirected.
    Example
    -------
        with spinner():
            do_something()
            do_something_else()
    """
    return Spinner(beep, disable, force)
