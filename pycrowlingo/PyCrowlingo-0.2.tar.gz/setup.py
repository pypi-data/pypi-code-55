from setuptools import setup, find_packages

with open("requirements.txt", 'r') as file:
    requirements = file.readlines()

setup(
    name='PyCrowlingo',
    version='0.2',
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        'rasa': ["rasa"]
    },
    license='copyright: Crowlingo',
    author='Jonas Bouaziz',
    description='Official Crowlingo SDK. Access to all NLP and NLU services that analyze texts regardless of the '
                'language. '
)
