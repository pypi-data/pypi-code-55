import os
from setuptools import setup

# moreutils
# Standard library augmenting utilities and helpers.


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="moreutils",
    version="0.0.1",
    description="Standard library augmenting utilities and helpers.",
    author="Johan Nestaas",
    author_email="johannestaas@gmail.com",
    license="GPLv3",
    keywords="stdlib utils",
    url="https://github.com/johannestaas/moreutils",
    packages=['moreutils'],
    package_dir={'moreutils': 'moreutils'},
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'moreutils=moreutils:main',
        ],
    },
)
