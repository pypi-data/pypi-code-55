import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
        name='Riseup Mail',
        version='0.001',
        author='m1ghtfr3e',
        description='Writing and Reading Riseup Mails',
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        url='https://github.com/m1ghtfr3e/RiseupMail',
        packages=setuptools.find_packages(),
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Programming Language :: Python :: 3',
            'Programming Language :: Unix Shell',
            'Topic :: Communications :: Email',
            'Topic :: Security',
            'Operating System :: OS Independent',
            ]
)
