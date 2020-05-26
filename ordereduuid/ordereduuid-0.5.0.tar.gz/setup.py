import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='ordereduuid',
    version='0.5.0',
    author='Jaron Powser',
    author_email='jpowser@abbotellis.com',
    description='Create time-ordered UUIDs ideal for database keys',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/abbot-ellis/ordered-uuid.git',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

