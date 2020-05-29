from setuptools import setup

setup(
    name='pycontentdb',
    version='0.1.1',
    packages=['pycontentdb'],
    url='https://gitlab.com/Niwla23/pycontentdb',
    download_url='https://gitlab.com/Niwla23/pycontentdb',
    license='MIT',
    author='Alwin Lohrie (Niwla23)',
    author_email='alwin.l@gmx.de',
    description='Retrieves Data from contentdb',
    keywords=['minetest', 'contentdb'],
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
