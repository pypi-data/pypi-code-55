import os
import json
from typing import TextIO, Iterable


class Console:
    def __init__(self, stream: TextIO, linesep=os.linesep):
        self.stream = stream
        self.linesep = linesep

    def print(self, text: str):
        self.stream.write(f"{text} {self.linesep}")

    def print_title(self, title):
        self.newln()
        self.print(f"{title}:")

    def print_iter(self, title: str, items: Iterable):
        self.print_title(title)
        self.newln()
        for item in items:
            self.print(f" - {item}")
        self.newln()

    def print_json(self, title: str, obj):
        self.print_title(title)
        self.newln()
        json.dump(obj, self.stream, indent=4)
        self.newln()

    def newln(self):
        self.print("")
