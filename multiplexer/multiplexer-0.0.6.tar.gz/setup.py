from setuptools import setup, find_namespace_packages

setup(
    name='multiplexer',
    version='0.0.6',
    description='[WIP] New cypher library.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mathix420/multiplexer',
    author='Arnaud Gissinger',
    author_email='agissing@student.42.fr',
    license='MIT',
    python_requires='>=3.6',
    classifiers=[
                'Intended Audience :: Developers',
                'Intended Audience :: System Administrators',

                'Development Status :: 4 - Beta',

                'Topic :: Security :: Cryptography',

                'License :: OSI Approved :: MIT License',

                'Programming Language :: Python :: 3 :: Only',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
                'Programming Language :: Python :: 3.8',
                'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'python-dotenv==0.10.5',
        'PyInquirer==1.0.3',
        'PyYAML>=3.13',
        'boto3>=1.11.6',
    ],
    packages=find_namespace_packages(include=["multiplexer", "multiplexer.*"]),
)