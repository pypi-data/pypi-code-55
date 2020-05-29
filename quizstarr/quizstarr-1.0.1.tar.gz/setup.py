from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_desc = f.read()

setup(
    name = 'quizstarr',
    version = '1.0.1',
    author = 'Samuel .O. Bamgbose',
    author_email = 'bsaintdesigns@gmail.com',
    description = ' A package that displays questions',
    long_description = long_desc,
    long_description_content_type = 'text/markdown',
    py_modules = ['quizzstarr'],
    classifiers = [
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    packages = find_packages(),
    python_requires = '>= 3.6',
    install_requires = ['requests'],
    entry_points = {
        'console_scripts' : [
            'quizstarr = quizstarr:__main__',
        ]
    }
)
