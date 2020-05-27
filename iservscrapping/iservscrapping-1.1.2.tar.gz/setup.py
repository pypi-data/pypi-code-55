from setuptools import setup

setup(
    name='iservscrapping',
    version='1.1.2',
    packages=['iservscrapping'],
    url='https://gitlab.com/schoolserver_redo_project/iservscrapping',
    download_url = 'https://gitlab.com/schoolserver_redo_project/iservscrapping/-/archive/master/iservscrapping-master.tar.gz',
    license='MIT',
    author='Alwin Lohrie (Niwla23)',
    author_email='alwin.l@gmx.de',
    description='This Scrapper can get data from iserv servers hosting Untis plans. (Common in germany)',
    keywords = ['iserv', 'school', 'api', 'scrapper'],
    install_requires=[
        'markdown',
        'pendulum',
        'requests',
        'bs4',
        'lxml',
        'requests_cache'
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
    ],
)
