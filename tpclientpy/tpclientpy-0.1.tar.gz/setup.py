from setuptools import setup, find_packages

setup(name='tpclientpy',
      version='0.1',
      description='TradePatio client',
      # packages=['requests', 'time', 'urllib', 'hashlib', 'hmac', 'math', 'tpclientpy'],
      packages=find_packages(exclude=['example']),
      author_email='darkfoxs96@gmail.com',
      zip_safe=False)
