from setuptools import setup
import sys
import urllib3

DISTNAME = 'pyspark-config'
DESCRIPTION = 'Configurable data pipeline with Pyspark'
with open('README.md') as f:
    LONG_DESCRIPTION = f.read()
AUTHOR = 'Patrizio Guagliardo'
AUTHOR_EMAIL = 'patrizio.guagliardo@gmx.de'
LICENSE = 'new BSD'
URL = 'https://github.com/Patrizio1301/pyspark-config'
VERSION = '0.0.2.14'

PYSPARK_MIN_VERSION = '2.4.5'
PYYAML_MIN_VERSION = '5.3.1'
DATACLASSES_MIN_VERSION = '0.0'
DATACLASSES_JSON_MIN_VERSION = '0.4.2'
MARSHMALLOW_MIN_VESION = '3.5.2'

def setup_package():
    metadata = dict(name=DISTNAME,
                    author=AUTHOR,
                    author_email=AUTHOR_EMAIL,
                    description=DESCRIPTION,
                    license=LICENSE,
                    url=URL,
                    include_package_data=True,
                    version=VERSION,
                    long_description=LONG_DESCRIPTION,
                    long_description_content_type="text/markdown",
                    packages=["pyspark_config",
                              "pyspark_config.input",
                              "pyspark_config.transformations",
                              "pyspark_config.output",
                              "pyspark_config.yamlConfig",
                              "pyspark_config.spark_utils"
                              ],
                    package_dir ={
                        "pyspark_config.input": 'pyspark_config/input',
                        "pyspark_config.transformations": 'pyspark_config/transformations',
                        "pyspark_config.output": 'pyspark_config/output',
                        "pyspark_config.yamlConfig": 'pyspark_config/yamlConfig',
                        "pyspark_config.spark_utils": 'pyspark_config/spark_utils'
                    },
                    classifiers=['Programming Language :: Python',
                                 'Topic :: Software Development',
                                 'Topic :: Scientific/Engineering',
                                 'Operating System :: Microsoft :: Windows',
                                 'Operating System :: POSIX',
                                 'Operating System :: Unix',
                                 'Operating System :: MacOS',
                                 'Programming Language :: Python :: 3',
                                 'Programming Language :: Python :: 3.6',
                                 'Programming Language :: Python :: 3.7',
                                 'Programming Language :: Python :: 3.8',
                                 ('Programming Language :: Python :: '
                                  'Implementation :: PyPy')
                                 ],
                    python_requires=">=3.6",
                    install_requires=[
                        'pyspark>={}'.format(PYSPARK_MIN_VERSION),
                        'PyYAML>={}'.format(PYYAML_MIN_VERSION),
                        'dataclasses>={}'.format(DATACLASSES_MIN_VERSION),
                        'dataclasses-json>={}'.format(DATACLASSES_JSON_MIN_VERSION),
                        'marshmallow>={}'.format(MARSHMALLOW_MIN_VESION),
                    ],
                    package_data={'': ['*.pxd']}
                    )
    
    #if len(sys.argv) >= 2 and ('--help' in sys.argv[1:] or
    #    sys.argv[1] in ('--help-commands', 'egg_info', '--version',
    #                    'clean')):
    ## Use setuptools for these commands (they don't work well or at all
    ## with distutils).  For normal builds use distutils.
    #    try:
    #        from setuptools import setup
    #    except ImportError:
    #        from distutils.core import setup

    setup(**metadata)

if __name__ == "__main__":
    setup_package()
