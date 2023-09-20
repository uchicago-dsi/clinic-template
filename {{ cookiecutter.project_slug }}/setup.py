from setuptools import find_packages, setup

setup(
    name="{{ cookiecutter.project_slug }}",
    version="0.1.0",
    packages=find_packages(include=["{{ cookiecutter.code_directory }}", "{{ cookiecutter.code_directory }}.*"]),
    install_requires=[],
)
