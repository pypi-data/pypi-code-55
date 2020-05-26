import contextlib
import os


class File:
    def __init__(self, file_path, create=False):
        self.file = file_path
        self._path_args = self.file.split("/")
        self.path = ""

        for arg in self._path_args[:-1]:
            self.path += arg + "/"

        self.file_name = self._path_args[-1]

        if create:
            if self.path != "":
                with contextlib.suppress(FileExistsError):
                    os.makedirs(self.path)
            try:
                with open(self.file, "r"):
                    pass
            except FileNotFoundError:
                with open(self.file, "w"):
                    pass

    def __repr__(self):
        return self.file

    def file_exists(self):
        os.path.isfile(self.file)

    def write(self, content, is_txt=True):
        method = "w" if is_txt else "wb"
        with open(self.file, method) as file:
            file.write(content)

    def read(self):
        with open(self.file, "r") as file:
            return file.read()

    def add(self, line):
        read = self.read()
        new_content = read + "\n" + line
        self.write(new_content)

    def delete_file(self):
        os.remove(self.file)
        del self

