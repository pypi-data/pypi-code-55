import setuptools

setuptools.setup(
    name='p1-harpocrates-sdk',
    version='0.2.5',
    packages=[
        'keychainClient',
        'keychainClient.model',
        'keychainClient.crypto',
        'keychainClient.exception',
        'keychainClient.protobuf',
        ],
    url='http://www.privacyone.co/',
    license='privacy one commercial licensing',
    author='Jing Chen',
    author_email='jing.chen@privacyone.co',
    description='p1 sdk of python',
    install_requires=[
        'requests',
        'cryptography',
        'cacheout',
        'protobuf',
      ],
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)
