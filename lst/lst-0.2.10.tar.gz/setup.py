import setuptools

with open('requirements.txt') as f:
	requires = list(f)

setuptools.setup(
    name='lst',
    version='0.2.10',
    author='Andriy Stremeluk',
    author_email='astremeluk@gmail.com',
    description='Declarative Scraping Tools',
    license="MIT",
    packages=setuptools.find_packages(exclude=['test*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    install_requires=requires,
    python_requires='>=3.5'
)
