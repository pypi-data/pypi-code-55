from setuptools import setup,find_packages, os

setup(
    name='deploy-task-definitions',
    version= os.environ['CIRCLE_TAG'],
    description='Script for deploy task definitions to ECS',
    url='https://github.com/redaptiveinc/deploy-task-definitions',
    author='Mariano Gimenez',
    author_email='mariano.gimenez@agileengine.com',
    license='unlicense',
    zip_safe=False,
    packages = find_packages(),
    entry_points ={
        'console_scripts': [
            'deploy-task-definitions = src.deployTaskDefinitions:main'
        ]
    },
    install_requires = [
        'requests==2.20.0',
        'pyhcl==0.3.12',
        'python-dotenv==0.10.3',
        'boto3==1.10.7',
        'botocore==1.13.9'

    ]
)
