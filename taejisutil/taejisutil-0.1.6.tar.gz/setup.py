import setuptools

setuptools.setup(
    name="taejisutil",
    version="0.1.6",
    license='MIT',
    author="cheolgi",
    author_email="mobilechos@gmail.com",
    description="utils",
    long_description=open('README.md').read(),
    url="http://www.mobilechos.com",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)