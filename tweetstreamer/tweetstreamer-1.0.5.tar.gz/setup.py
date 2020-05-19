# pylint: disable-msg=no-name-in-module,import-error
from distutils.cmd import Command
from os import getcwd
from re import search
from subprocess import check_call
from setuptools import find_packages, setup

class PylintCommand(Command):
    description = 'run pylint on Python source files'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        command = ['pylint', getcwd()]
        return check_call(command)

def get_meta_data():
    meta_data_file = "tweetstreamer/__init__.py"
    def parse_meta_data(matched_string, meta_data_type):
        if matched_string:
            return matched_string.group(1)
        raise RuntimeError("Unable to find {0} string in {1}".format(
            meta_data_type, meta_data_file
        ))

    f = open(meta_data_file, 'r', encoding='utf-8')
    file_text = f.read()
    f.close()
    version_match = search(r"__version__ = ['\"]([^'\"]*)['\"]", file_text)
    author_match = search(r"__author__ = ['\"]([^'\"]*)['\"]", file_text)
    license_match = search(r"__license__ = ['\"]([^'\"]*)['\"]", file_text)

    return {
        'version': parse_meta_data(version_match, 'version'),
        'author': parse_meta_data(author_match, 'author'),
        'license': parse_meta_data(license_match, 'license')
    }


def get_short_description():
    return 'A Tweepy streamer to collect tweets from Twitter\'s ' + \
        'Streaming API based on criteria'

def get_long_description():
    readme_file = 'README.md'
    with open(readme_file, 'r', encoding='utf-8') as f:
        readme = f.read()
    return readme

meta_data = get_meta_data()

setup(
    name='tweetstreamer',
    packages=find_packages(),
    version=meta_data['version'],
    description=get_short_description(),
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    license=meta_data['license'],
    author=meta_data['author'],
    author_email='mail@suddi.io',
    url='https://github.com/suddi/tweetstreamer',
    download_url='https://github.com/suddi/tweetstreamer',
    keywords=[
        'twitter',
        'streamer',
        'streaming',
        'api',
        'tweet',
        'tweets',
        'tweepy',
        'tweetstream',
        'tweetstreamer'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8'
    ],
    cmdclass={
        'lint': PylintCommand
    }
)
