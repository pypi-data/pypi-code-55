import os


class DefaultConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
