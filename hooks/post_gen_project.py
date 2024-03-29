import os
import shutil

use_cluster = "{{ cookiecutter.cluster }}" == "yes"
use_docker = "{{ cookiecutter.docker }}" == "yes"
create_example_files = "{{ cookiecutter.examples }}" == "yes"

if not use_cluster:
    shutil.rmtree("config")

if not use_docker:
    os.remove("Dockerfile")

if not create_example_files:
    os.remove("{{ cookiecutter.code_directory }}/pipeline_example.py")
    os.remove(
        "{{ cookiecutter.code_directory }}/preprocess_util_lib_example.py"
    )
    os.remove("notebooks/Test.ipynb")
