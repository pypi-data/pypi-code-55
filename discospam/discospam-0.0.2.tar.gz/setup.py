from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='discospam',
    version='0.0.2',
    description='Simple library for spamming and deleting discord webhooks.',
    Long_description="""
Test
    """,
    url='',
    author='FliiGQ',
    author_email='fliigq@flii.gq',
    License='MIT',
    classifiers=classifiers,
    keywords='webhooks',
    packages=find_packages(),
    install_requires=['requests']
)