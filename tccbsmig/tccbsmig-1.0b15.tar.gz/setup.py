import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='tccbsmig',
    version='1.0b15',
    description='CBS Data Migration to Encrypted Disk',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    author='Minze Tao',
    author_email='minzetaos@tencent.com',
    license='MIT',
    include_package_data=True,
    install_requires=['paramiko', 'tencentcloud-sdk-python'],
    entry_points ={
            'console_scripts': [
                'tccbsmig = tccbsmig.ebs_en:main'
            ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    keywords ='Python CBS Ecryption Migration'

    )
