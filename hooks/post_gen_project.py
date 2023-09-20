import shutil
import os

use_cluster = "{{ cookiecutter.cluster }}" == "yes"
use_docker = "{{ cookiecutter.docker }}" == "yes"
do_smoke_test = "{{ cookiecutter.smoke_test }}" == "yes"

if not use_cluster:
    shutil.rmtree("config/query")

if not use_docker:
    os.remove("{{ cookiecutter.code_directory }}/Dockerfile")
    os.remove("notebooks/Dockerfile")

if not do_smoke_test and not use_cluster:
    os.remove("{{ cookiecutter.code_directory }}/main.py")

if not do_smoke_test:
    os.remove("{{ cookiecutter.code_directory }}/preprocess.py")
    os.remove("notebooks/Test.ipynb")
