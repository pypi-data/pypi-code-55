import setuptools

setuptools.setup(
    name="lalsi",
    version="0.0.1",
    author="Krishna",
    author_email="krishna.vijay4444@gmail.com",
    description="Pythonic Makefile",
    long_description=open('README.rst').read(),
    keywords=['alternative to makefile', 'makefile alternative', 'python makefile'],
    platforms=['any'],
    scripts=['bin/lalsi'],
    license='MIT License',
    long_description_content_type="text/x-rst",
    url="https://krishkasula.gitlab.io/lalsi/index.html",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
