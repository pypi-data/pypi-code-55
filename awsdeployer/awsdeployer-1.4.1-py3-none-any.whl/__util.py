import os
import random
import string
import zipfile


def zip_directory(ziph, path):
    for root, _, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def zip_function(files):
    zip_name = 'temp-' + random_string(32) + '.zip'

    # create zip with all files
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for file in files:
        zipf.write(file)
    zipf.close()

    # read file to return
    data = read_file(zip_name)

    # remove zip file, not needed
    os.remove(zip_name)

    return data


def read_file(name):
    with open(name, 'rb') as file:
        return file.read()


def random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


def build_path(parts):
    if len(parts) == 0:
        return '/'

    string = ''
    for part in parts:
        string += '/' + part
    return string
