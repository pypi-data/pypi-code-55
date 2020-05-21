import setuptools
from pathlib import Path
setuptools.setup(
    name="bullet_gym",
    version='0.0.1',
    description="A OpenAI Gym Env for pandas",
    packages=setuptools.find_packages(include="bulletgym*"),
    install_requires=['gym','pybullet']
)