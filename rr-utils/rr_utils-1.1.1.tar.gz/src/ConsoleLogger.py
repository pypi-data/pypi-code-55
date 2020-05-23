import sys


class ConsoleLogger(object):
    def __init__(self):
        self.log_destination = [sys.stdout]

    def add_log_file_destination(self, filename):
        self._add_log_destination(open(filename, "a"))
        return self

    def remove_last_destination(self):
        if len(self.log_destination) <= 1:
            raise Exception()
        last = self.log_destination.pop()
        last.flush()
        last.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remove_last_destination()
        return self

    def write(self, message):
        for item in self.log_destination:
            item.write(message)

    def flush(self):
        for item in self.log_destination:
            item.flush()

    def _add_log_destination(self, destination):
        self.log_destination.append(destination)