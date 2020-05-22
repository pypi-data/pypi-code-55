import argparse
import datetime
import sys
import threading
import time

from deepdiff import DeepDiff
from sentry_sdk import capture_exception, init

from . import api
from .globals import set_config
from .analyzer import Analyzer


def flush_print(line):
    print(datetime.datetime.now().isoformat(), line)
    sys.stdout.flush()


def flush_write(message):
    sys.stdout.write(message)
    sys.stdout.flush()


def spinning_cursor():
    while True:
        for cursor in "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁":
            yield cursor


class Coordinator:
    def __init__(self, converter, path: str):
        self.analyzers = {}
        self.converter = converter
        self.path = path
        self.running = False
        self.parser = argparse.ArgumentParser(
            description="Create a Centroid Ambulation analysis for the BehaviorCloud platform."
        )
        self.parser.add_argument(
            "--host",
            nargs="?",
            required=True,
            help="The hostname of the BehaviorCloud api server. "
            + "Typically, this is api.behaviorcloud.com.",
        )
        self.parser.add_argument(
            "--token",
            nargs="?",
            required=True,
            help="The JWT token provided by the BehaviorCloud platform.",
        )
        self.parser.add_argument("--id", nargs="?", help="The queued analysis id.")
        self.parser.add_argument(
            "--daemon",
            action="store_true",
            help="Run this analyzer is a daemonized mode, watching for new jobs.",
        )
        self.parser.add_argument(
            "--runtests",
            action="store_true",
            help="Rerun public analyses comparing this analyzer's results to existing results.",
        )

    def analyze(self, queued_analysis_id):
        if queued_analysis_id in self.analyzers:
            return
        analyzer = Analyzer(queued_analysis_id, self.converter)
        self.analyzers[queued_analysis_id] = analyzer

        flush_print("Starting Converting Queued Analysis: %s" % (queued_analysis_id))
        try:
            analyzer.start()
            flush_print("Finished Converting Queued Analysis: %s" % (queued_analysis_id))
            return True
        except Exception as e:
            capture_exception(e)
            flush_print("Error Converting Queued Analysis: %s" % (queued_analysis_id))

        return False

    def run(self):
        arguments = self.parser.parse_args()
        set_config({"HOST": arguments.host, "TOKEN": arguments.token, "API_VERSION": "1.1"})

        init("https://5196a2999eb1497a8fd043d2683e30c0@sentry.io/1298461")

        if arguments.id:
            self.analyze(arguments.id)
        elif arguments.daemon:
            self.start_daemon()
        elif arguments.runtests:
            self.runtests()
        elif arguments.createtests:
            self.createtests()
        else:
            flush_print("You must supply an id when not using daemon or test mode")

    def start_daemon(self):
        if self.running:
            return
        self.running = True
        flush_print("Starting analysis daemon")
        t = threading.Thread(target=self.daemon)
        t.start()

    def daemon(self):
        spinner = spinning_cursor()

        while self.running:
            queued_analyses = api.get_queued_analysis_index(self.path)
            ran = False
            for queued_analysis in queued_analyses:
                if queued_analysis["ended"]:
                    continue
                id = queued_analysis["id"]
                ran = self.analyze(id)
            if not ran:
                for _ in range(15):
                    message = next(spinner) + " waiting for analyses..."
                    flush_write(message)
                    time.sleep(0.1)
                    [sys.stdout.write("\b") for x in message]

    def runtests(self):
        queued_analyses = api.get_queued_analysis_index(self.path, ended=True, public=True)
        flush_print("Found %s public %s analyses" % (len(queued_analyses), self.path))

        for queued_analysis in queued_analyses:
            id = queued_analysis["id"]
            analyzer = Analyzer(id, self.converter)
            result, old, new = analyzer.test()
            if result:
                flush_print("Passed: Queued Analysis %s" % (id))
            else:
                flush_print("Failed: Queued Analysis %s" % (id))
                flush_print(DeepDiff(old, new))
                sys.exit(1)

        sys.exit(0)

    def stop(self):
        self.running = False
