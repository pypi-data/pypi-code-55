import subprocess
import shlex
import logging


def call(command):
    logging.debug(command)
    subprocess.call(shlex.split(command))


def check_call(command):
    logging.debug(command)
    subprocess.check_call(shlex.split(command))


def run(command):
    logging.debug(command)
    return subprocess.run(shlex.split(command), stdout=subprocess.PIPE).stdout.decode('utf-8')
