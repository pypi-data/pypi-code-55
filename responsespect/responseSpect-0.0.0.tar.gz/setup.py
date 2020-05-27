from setuptools import setup, find_packages
from setuptools.extension import Extension
from os import path


setup(
    name='responseSpect',  # Required

    version='0.0.0',  # Required

    description='acceleration,velocity and displacement response spectra calculation',  # Optional
    url='https://github.com/Junjun1guo/responseSpect',  # Optional

    author='Junjun Guo',  # Optional
    author_email='guojj01@gmail.com',  # Optional

    classifiers=[  # Optional
 
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='response sepctra, accelearion,velocity,displacement',  # Optional

    packages=find_packages(),  # Required
    python_requires='>=3.6', 
	setup_requires=[
		'numpy>=1.17.4'
		],
    package_data={  # Optional
        '':['*.dll'],
    },
	zip_safe=False
)