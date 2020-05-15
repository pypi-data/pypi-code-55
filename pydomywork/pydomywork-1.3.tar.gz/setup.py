from distutils.core import setup
import setuptools

def readme():
    with open(r'README.txt') as f:
        README = f.read()
    return README

setup(
    name = 'pydomywork',
    packages = setuptools.find_packages(),
    version = '1.3',
    license='MIT',
    description = 'This library converts computer characters to handwritten characters.',
    author = 'Ankit Raj Mahapatra',
    author_email = 'ankitrajjitendra816@gmail.com',
    url = 'https://github.com/Ankit404butfound//HomeworkMachine',
    download_url = 'https://github.com/Ankit404butfound/HomeworkMachine/archive/1.0.tar.gz',
    keywords = ['convert_text', 'img_to_handtxt', 'download', 'getimg'],
    install_requires=[           
          'pytesseract',
          'opencv-python',
          'numpy',
          'keyboard',
          'pillow',
      ],
    include_package_data=True,
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    ],
)
