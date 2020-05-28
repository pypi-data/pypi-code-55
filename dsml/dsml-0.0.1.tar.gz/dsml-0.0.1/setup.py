from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3'
]

setup(
    name='dsml',
    version='0.0.1',
    descroption='a neural network implementation',
    url='',
    author='Hali Lev Ari',
    author_email='LevAri.Hali@gmail.com',
    license='Apache 2.0',
    classifiers=classifiers,
    packages=find_packages(),
    keywords=['neural network','machine learning'],
    install_requiers=['numpy']
)
