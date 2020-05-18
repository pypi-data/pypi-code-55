import setuptools

setuptools.setup(
    name="amazon_selenium",
    version="0.1.2",
    author="Kovács Kristóf-Attila",
    description="amazon_selenium",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/amazon_selenium",
    packages=setuptools.find_packages(),
    install_requires=["selenium_firefox", "kov_utils"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)