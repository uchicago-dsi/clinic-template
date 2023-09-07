from setuptools import find_packages, setup

setup(
    name="clinic-sample",
    version="0.1.0",
    packages=find_packages(include=["project", "project.*"]),
    install_requires=[],
)
