import setuptools

setuptools.setup(
    name="swatchtime",
    version="0.5",
    author="T.J. Bay",
    license="MIT",
    author_email="spintronic@gmail.com",
    description="Calculates Swatch Internet Time",
    url="https://github.com/tjbay/swatchtime",
    download_url="https://github.com/tjbay/swatchtime/archive/0.5.tar.gz",
    keywords=["Swatch", "Internet", "Time"],
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['swatchtime=swatchtime.command_line:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",

    ],
    python_requires='>=3.0',
)
