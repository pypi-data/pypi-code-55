""" setup module.

"""

from distutils.core import setup

setup(
    name='glimmer',
    packages=['glimmer'],
    version='0.0.1',
    license='MIT',
    description='Glimmer is a library built to implement content management systems for python web applications.',
    author='Joshua Sello',
    author_email='joshuasello@gmail.com',
    url='https://github.com/joshuasello/glimmer',
    download_url='https://github.com/joshuasello/glimmer/archive/v0.0.1.tar.gz',
    keywords=["flask", "content management", "web development", "website", "cms", "framework"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
