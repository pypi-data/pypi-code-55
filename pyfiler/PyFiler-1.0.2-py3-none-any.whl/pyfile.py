import os
from threading import Thread
from .file import File


class PyFile(File):
    def __init__(self, file_path, create=False):
        super().__init__(file_path, create)
        self.running_thread = None

    @property
    def running(self):
        return True if self.running_thread is not None else False

    def add_code(self, line, indents=0, indent_size=4):
        read = self.read()
        indent = " " * indent_size * indents
        new_content = bytes(indent + read + "\n" + line, "utf-8")
        self.write(new_content, is_txt=False)

    def import_attr(self, attr):
        return __import__(self.file.replace("/", ".", len(self.file)), fromlist=[]).__getattribute__(attr)

    def run(self):
        Thread(target=lambda: os.system(f"python {self.file}")).start()
