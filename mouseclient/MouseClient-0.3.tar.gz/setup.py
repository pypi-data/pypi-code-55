from setuptools import setup


requires = ["requests>=2.22.0"]


setup(
    name='MouseClient',
    version='0.3',
    description='Client program for micro mouse simulation',
    url='https://www.osumoi-stdio.com/maze/',
    author='Takaomi Konishi',
    author_email='takaomikonishi0626@gmail.com',
    license='MIT',
    keywords='micromouse simulation client',
    packages=[
        "MazeSimulator",
    ],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
