from setuptools import setup, find_packages

setup(
    name='peony',
    version='1.0.1',
    zip_safe=False,
    platforms='any',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    python_requires='>=3',
    install_requires=['setproctitle', 'twisted', 'events', 'netkit', 'click'],
    url='https://github.com/dantezhu/peony',
    license='MIT',
    author='dantezhu',
    author_email='zny2008@gmail.com',
    description='',
)
