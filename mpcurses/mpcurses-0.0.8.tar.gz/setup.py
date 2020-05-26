#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'mpcurses',
        version = '0.0.8',
        description = 'A framework that exposes a simple set of APIs enabling multi-process integration with the curses screen painting library',
        long_description = '\nmpcurses is a framework that exposes a simple set of APIs enabling multi-process integration with the curses screen painting library.\n\nWith mpcurses, the complexities of setting up multi-processing within a curses environment are abstracted into a few simple APIs and constructs. The main features:\n\n* Execute a method across one or more concurrent processes\n* Queue method execution to ensure only a predefined number of processes are running\n* Define `curses` screen layout using a Python dict\n* Leverage built-in directives for updating screen dynamically\n  * Keep numeric counts\n  * Update text values\n  * Update text colors\n  * Maintain visual indicators\n  * Update progress bars\n  * Display table of data coming from concurrent proceses\n\n**How it works**\n\nThe method you wish to execute concurrently is decorated with the queue handler decorator. The queue handler decorator creates a new log handler that will write all logged messages within the decorated method to a thread-safe queue. The main process creates the thread-safe message queue and handles the spawning of the desired number of concurrent processes, each process will be passed the reference to the message queue upon startup. As the process executes it will send all log messages to the message queue. The main process will then read messages from the message queue as they come in and update the curses screen accordingly.\n\nThe layout of the curses screen is defined as a dictionary and can leverage builtin constructs for capturing messages, incrementing counters, and processing side effects such as changing text colors when certain messages appear. The result is a screen that is being updated dynamically from one or more concurrent processes running in the background.\n\nFor samples checkout our home page: https://github.com/soda480/mpcurses\n',
        author = 'Emilio Reyes',
        author_email = 'emilio.reyes@intel.com',
        license = 'Apache License, Version 2.0',
        url = 'https://github.com/soda480/mpcurses',
        scripts = [],
        packages = ['mpcurses'],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: Console :: Curses',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Networking',
            'Topic :: System :: Systems Administration'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )
