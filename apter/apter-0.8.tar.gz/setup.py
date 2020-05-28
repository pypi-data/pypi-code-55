from setuptools import setup, find_packages

APP_NAME = 'apter'

# noinspection SpellCheckingInspection
setup(
    name=APP_NAME,
    # version managed by release script
    version='0.8',
    description='A sweet project configuration package',
    url='https://github.com/ulygit/apter',
    author='U. Melendez',
    author_email='apterpy@bfjournal.com',
    license='MIT',
    packages=find_packages(exclude=['test']),
    py_modules=['apter'],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest'
    ],
    install_requires=[
        'parse', 'PyYaml'
    ],
)
