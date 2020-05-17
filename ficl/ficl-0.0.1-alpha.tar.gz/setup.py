from distutils.core import setup

setup(
        name = 'ficl',
        packages = ['ficl'],
        version = '0.0.1-alpha',
        license = 'GPLv3',
        description = 'Empty large batches of files in one command',
        author = 'Andrew Titenko',
        author_email = 'contact.me@arkadyt.dev',
        url = 'https://github.com/arkadyt/ficl',
        download_url = 'https://github.com/arkadyt/ficl/archive/0.0.1-alpha.tar.gz',
        keywords = ['quick', 'easy', 'batch', 'empty', 'clean', 'file', 'files'],
        install_requires = [
                'textwrap3',
                'argparse'
        ],
        classifiers = [
                'Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
                'Topic :: System :: Filesystems',
                'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 3'
        ]
)
