class MyReader:
    def __init__(self, source_path, file_type=None):
        self.source = source_path
        self.extension_from_filename = source_path.split(".")[-1]
        self.__possible_extension = ["csv", "npy", "npz", "feather", "ftr", "pickle", "pkl", "json", "xlsx", "excel",
                                     "str"]
        if file_type is None:
            if self.extension_from_filename not in self.__possible_extension:
                raise KeyError("give a proper file_type")
            else:
                pass
        else:
            if file_type not in self.__possible_extension:
                raise KeyError("give a proper file_type")
            else:
                pass

    def print_extensions(self):
        print(self.__possible_extension)

    def str(self):
        with open(self.source, 'r') as f:
            result = f.read()
        return result

    def json(self):
        import json
        with open(self.source, 'r') as f:
            result = json.load(f)
        return result

    def pickle(self):
        import pickle
        with open(self.source, 'rb') as f:
            result = pickle.load(f)
        return result

    def numpy(self):
        import numpy as np
        return np.load(self.source)

    def feather(self):
        import feather
        return feather.read_dataframe(self.source)
