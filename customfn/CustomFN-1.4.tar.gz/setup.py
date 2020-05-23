from setuptools import setup,find_packages

setup(
    name='CustomFN',
    version='1.4',
    description='Fortnite Bot',
    url='https://github.com/JaniniRami07/CustomFN/archive/1.4.tar.gz',
    author_email='janinirami@tutanota.com',
    packages=find_packages(),
    install_requires=['fortnitepy==1.7.1','sanic','requests','aiofiles']
)
