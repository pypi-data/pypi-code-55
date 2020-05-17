import os


PKG_DIR = os.path.abspath(os.path.dirname(__file__))


def clouds_dirs():
    yield os.path.join(PKG_DIR, 'clouds')
