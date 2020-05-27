from setuptools import setup, find_packages

setup(name='exprlib',
      version='0.1a2',
      url='https://github.com/crocodile850/ExprLib',
      license='MIT',
      author='LuteVasyl',
      author_email='crocodile21@gmail.com',
      packages=find_packages(exclude=['tests']),
      # description='Convert expression from infix form to binary tree and vice versa.',
      # long_description=open('README.md').read(),
      # classifiers=[
      #     "Programming Language :: Python :: 3",
      #     "License :: OSI Approved :: MIT License",
      # ],
      python_requires='>=3.6')
