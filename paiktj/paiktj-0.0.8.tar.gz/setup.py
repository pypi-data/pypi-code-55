import setuptools

setuptools.setup(
    name='paiktj',
    version='0.0.8',
    description='slight variation from builtin modules',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
    ],
    license='BSD',
    python_requires='>=3',
    install_requires=['numpy >= 1.17',
                      'scikit-learn >= 0.16',
                      'scipy >= 0.19',
                      'matplotlib >= 3.1',
                      'cryptography >= 2.0',
                      'seaborn >= 0.10'
                      ],

    author='paiktj',
    author_email='paiktj@snu.ac.kr',
    packages=setuptools.find_packages(),
)
