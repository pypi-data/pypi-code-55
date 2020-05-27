from setuptools import setup

setup(
    name="pysvglib",
    version="0.2.0",
    description="SVG drawing library",
    long_description="A library for programattically creating SVG graphics from basic shapes",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Graphics',
    ],
    keywords='svg graphics',
    url='https://github.com/gbingersoll/pysvglib',
    author='Greg Ingersoll',
    author_email='greg.ingersoll@convolutionresearch.com',
    license='MIT',
    packages=['svg'],
    extras_require={
        'dev': ['pytest', 'pycodestyle', 'setuptools', 'wheel']
    }
)
