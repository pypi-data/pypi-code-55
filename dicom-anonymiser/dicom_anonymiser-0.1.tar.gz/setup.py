"""dicom_anonymiser setup"""

import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Eric Pace",
    author_email="ericpace@pm.me",
    name='dicom_anonymiser',
    license="GNU GPLv3",
    description='dicom_anonymiser anonymises dicom files and folders with user customisable tags.',
    version='v0.1',
    long_description='dicom_anonymiser anonymises dicom files and folders with user customisable tags.',
    url='https://github.com/ericpace/dicom_anon_tool',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={'gui_scripts': ['anon=dicom_anonymiser.__main__:main']},
    python_requires=">=3.5",
    # Enable install requires when publishing on the normal PyPi
    install_requires=[
        'Gooey',
        'pydicom'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)