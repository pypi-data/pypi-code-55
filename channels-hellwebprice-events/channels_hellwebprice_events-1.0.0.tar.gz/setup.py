from setuptools import setup, find_packages
 
setup(name='channels_hellwebprice_events',
      version='1.0.0',
      url='https://github.com/hellwebprice/django_hellwebprice_events',
      license='MIT',
      author='HellWebPrice',
      author_email='hellwebprice@gmail.com',
      description='Events on django channels',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)