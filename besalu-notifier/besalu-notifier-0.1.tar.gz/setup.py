from setuptools import setup

setup(
    name='besalu-notifier',
    author='Alex Schokking',
    author_email = "aschokking@gmail.com",
    license = "MIT",
    version='0.1',
    url="https://github.com/aschokking/besalu-notifier",
    py_modules=['cli'],
    install_requires=[
        'Click',
        'notify-run'
    ],
    entry_points='''
        [console_scripts]
        besalu=cli:cli
    ''',
)