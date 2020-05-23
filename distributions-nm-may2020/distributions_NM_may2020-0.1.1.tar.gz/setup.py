from setuptools import setup

with open("distributions_NM_may2020/README.md", "r") as fh:
    long_description = fh.read()

setup(name='distributions_NM_may2020',
      version='0.1.1',
      description='Gaussian and Binomial distributions',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['distributions_NM_may2020'],
      author = 'Nuria Malet Quintar',
      author_email = 'maletq.ds@gmail.com',
      python_requires='>=3.0',
      zip_safe=False)
