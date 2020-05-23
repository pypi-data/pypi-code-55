import sys
from Constraints.BaseChecker import _BaseChecker
from Constraints.Exceptions import CheckerError


class Constraints:
    def __init__(self):
        self._conditions = []

    def add(self, checker_obj: _BaseChecker):
        self._conditions.append(checker_obj)

    def check(self, terminate_on_error=False):
        try:
            for item in self._conditions:
                item.check()
            return True
        except CheckerError as ex:
            if terminate_on_error:
                self._terminate(ex)
            raise ex

    @staticmethod
    def _terminate(ex):
        print("Problem with: {}".format(ex), file=sys.stderr)
        sys.exit(1)

