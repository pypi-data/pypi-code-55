# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="happydevelopperfr_flyplanner",
    version="0.0.5",
    description="fly planner for happy.developper.fr",
    author="COTTET Julien",
    author_email="happy.developper.fr@gmail.com",
    url="https://github.com/happy-developer-fr/fly-planner",
    packages=["flyplanner"],
)
