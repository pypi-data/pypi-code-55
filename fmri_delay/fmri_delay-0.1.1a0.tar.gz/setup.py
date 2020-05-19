from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='fmri_delay',
      version='0.1.1_a',
      description='Tool for measuring delay between sparse transitions in fmri BOLD signals',
      long_description='Tool for measuring delay between sparse transitions in fmri BOLD signals',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
      ],
      keywords='fmri neuroimaging delay',
      url='',
      author='Alexandre Cionca',
      author_email='cionkito@gmail.com',
      license='MIT',
      packages=['fmri_delay'],
      install_requires=[
      'numpy', 'scipy'
      ],
      include_package_data=True,
      zip_safe=False)