import setuptools

setuptools.setup(
    name="organizer-girvel",
    version="1.0.0",
    author="girvel",
    author_email="widauka@yandex.ru",
    description="This is very simple logging application for tracking your daily activities",
    url="https://github.com/girvel/organizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["termcolor", "text-actions-girvel"]
)
