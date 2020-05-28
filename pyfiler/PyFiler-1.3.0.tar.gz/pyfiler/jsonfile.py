from .file import File
from json import load, dump


class JSONFileError(Exception):
    pass


class JSONFile(File):
    def __init__(self, file_path, create=False):
        super().__init__(file_path, create=create)
        if not self.file.endswith(".json"):
            raise JSONFileError(f"{self.file} isn't a json file.")

    @property
    def json_type(self):
        with open(self.file, "r") as file:
            jfile = load(file)

        return jfile.__class__.__name__

    def read(self):
        with open(self.file, "r") as file:
            return load(file)

    def write(self, content):
        with open(self.file, "w") as file:
            dump(content, file)

    def add(self, element):
        with open(self.file, "r") as file:
            jfile = load(file)

        if self.json_type == "list":
            jfile.append(element)
        elif self.json_type == "dict":
            if len(element) == 2:
                jfile[element[0]] = element[1]
            else:
                raise JSONFileError("Invalid dictionary item element passed. Must be form (key, value).")

        with open(self.file, "w") as file:
            dump(jfile, file)

    def edit_value(self, key_or_index, new_value):
        if self.json_type in ["dict", "list"]:
            with open(self.file, "r") as file:
                jfile = load(file)

            jfile[key_or_index] = new_value

            with open(self.file, "w") as file:
                dump(jfile, file)
        else:
            raise JSONFileError("Error with json file.")