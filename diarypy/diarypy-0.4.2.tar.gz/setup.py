from distutils.util import convert_path
import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

main_ns = {}
ver_path = convert_path('diarypy/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setuptools.setup(
    name='diarypy',
    version=main_ns['__version__'],
    author='Miquel Perello Nieto',
    author_email='perello.nieto@gmail.com',
    description='Diary to create notebooks and store intermediate results and figures',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/perellonieto/DiaryPy',
    packages=setuptools.find_packages(),
    download_url='https://github.com/perellonieto/DiaryPy/archive/{}.tar.gz'.format(main_ns['__version__']),
    keywords=['diary', 'notebook', 'logging', 'figures', 'experiments'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
