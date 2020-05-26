import os
import shutil
from threading import Thread
from .file import File


class PyFileError(Exception):
    pass


class PyFile(File):
    def __init__(self, file_path, create=False):
        super().__init__(file_path, create)
        self.running_thread = None

    @property
    def running(self):
        if not self.running_thread.is_alive():
            self.running_thread = None
        return True if self.running_thread is not None else False

    def add_line(self, line, indents=0, indent_size=4):
        read = self.read()
        indent = " " * indent_size * indents
        new_content = bytes(indent + read + "\n" + line, "utf-8")
        self.write(new_content, is_txt=False)

    def add_lines(self, lines=None, indents=None, indent_size=4):
        if indents is None:
            indents = []
        if lines is None:
            lines = []

        if len(indents) != len(lines):
            raise ValueError("Length of lines doesn't match length of indents.")

        for i in range(len(lines)):
            self.add_line(lines[i], indents=indents[i], indent_size=indent_size)

    def edit_line(self, line_num, new_line):
        with open(self.file, "wb") as file:
            lines = self._get_all_lines()
            try:
                lines.pop(line_num)
            except IndexError:
                raise PyFileError(f"Line {line_num} doesn't exist in file {self.file}")
            lines.insert(new_line + "\r\n")
            new_file = ""
            for line in lines:
                new_file += line

            file.write(bytes(new_file, "utf-8"))

    def get_line(self, line_num):
        return self._get_all_lines()[line_num]

    def _get_all_lines(self):
        with open(self.file, "rb") as file:
            file_read = file.readlines()
        lines = []
        for char in range(len(file_read)):
            line = file_read[char]
            if not char == len(file_read) - 1:
                lines.append(line[0:len(line) - 2])
            else:
                lines.append(line)
        return lines

    def clear_line(self, line_num):
        self.edit_line(line_num, "")

    def clear_all(self):
        with open(self.file, "w"):
            pass

    def duplicate(self, to_dir):
        shutil.copyfile(self.file, to_dir)

    def run(self):
        self.running_thread = Thread(target=lambda: os.system(f"python {self.file}"))
        self.running_thread.start()
