from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'smallbrowser',
    packages = ['smallbrowser'],
    version = '0.1.7',
    license ='gpl-3.0',
    description = "A small HTTP browser library in Python based on the 'requests' library",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'Ivan Dustin B. Bilon',
    author_email = 'ivan22.dust@gmail.com',
    url = 'https://github.com/ivandustin/smallbrowser',
    keywords = ['http', 'browser', 'client', 'requests', 'pyquery',],
    install_requires=[
        'requests',
        'pyquery',
        ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        ],
    project_urls={
        'Documentation': 'https://github.com/ivandustin/smallbrowser',
        'Source': 'https://github.com/ivandustin/smallbrowser',
    },
)
