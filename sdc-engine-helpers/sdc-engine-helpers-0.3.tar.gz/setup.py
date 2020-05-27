"""
    Set up the sdc_engine_helpers package
"""
from setuptools import setup

setup(
    name='sdc-engine-helpers',
    packages=[
        'sdc_engine_helpers.maintenance',
        'sdc_engine_helpers.event',
        'sdc_engine_helpers.recommendations'
    ],
    install_requires=[
        'pymysql',
        'redis',
        'boto3',
        'sdc-helpers'
    ],
    description='AWS Recommendation Engine Helpers',
    version='0.3',
    url='http://github.com/RingierIMU/sdc-recommend-engine-helpers',
    author='Ringier South Africa',
    author_email='tools@ringier.co.za',
    keywords=['pip', 'helpers', 'aws', 'recommendation'],
    download_url='https://github.com/RingierIMU/sdc-recommend-engine-helpers/archive/v0.3.zip'
)
