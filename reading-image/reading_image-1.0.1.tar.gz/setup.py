from setuptools import setup
import os
import re
import io

def readme():
    with io.open('README.md', encoding="utf-8") as f:
        return f.read()

def description():

    with open(os.path.join("reading_image", "__init__.py"), 'r') as init_file:
        text = init_file.read()

    for i, m in enumerate(re.finditer("\"\"\"", text)):
        if i==0: start = m.end()
        if i==1: end = m.start()
        if i==2: break

    description = text[start:end]
    description = description.replace("\n", " ")

    return description

def version():

    with open(os.path.join("reading_image", "__init__.py"), 'r') as init_file:

        VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
        mo = re.search(VSRE, init_file.read(), re.M)

    return mo.group(1)

setup(
    name='reading_image',
    version=version(),
    description=description(),
    long_description=readme(),
    long_description_content_type='text/markdown',
    keywords='ReadingImage text analysis ocr nlp pdf image extraction table entity recognition translation',
    url='http://bitbucket.org/DannyHoskin/reading_image_python',
    author='Danny Hoskin',
    author_email='contact@nihsko.com',
    license='Nihsko',
    packages=['reading_image'],
    install_requires=[
        'pandas'
    ],
    include_package_data=True,
    zip_safe=False
)
