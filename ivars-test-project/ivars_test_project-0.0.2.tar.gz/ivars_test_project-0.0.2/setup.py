from setuptools import setup

setup(name='ivars_test_project',
      version='0.0.2',
      description='Ivars Test Project',
      url='http://github.com/ivargr/ivars_test_project',
      author='Ivar Grytten',
      author_email='',
      license='MIT',
      zip_safe=False,
      install_requires=['numpy', 'python-coveralls', 'pyvg',
                        'pyfaidx', 'offsetbasedgraph==2.1.4', 'tqdm', 'scipy'],
      classifiers=[
            'Programming Language :: Python :: 3'
      ],
      entry_points = {
        'console_scripts': ['ivars_test_project=ivars_test_project.command_line_interface:main'],
      }
)