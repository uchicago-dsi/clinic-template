import os
import shutil
from datetime import datetime

use_cluster = "{{ cookiecutter.cluster }}" == "yes"
use_docker = "{{ cookiecutter.docker }}" == "yes"
use_data_dir = "{{ cookiecutter.data_dir }}" != "none"
use_local_data_dir = "{{ cookiecutter.data_dir }}" == "local"
create_example_files = "{{ cookiecutter.examples }}" == "yes"
keep_bsd3 = f"{{ cookiecutter.bsd }}" == "yes"
use_annotations = f"{{ cookiecutter.ann }}" == "yes"

if not use_cluster:
    shutil.rmtree("config")

if not use_docker:
    os.remove("Dockerfile")
    os.remove("docker-compose.yaml")

if not use_data_dir:
    os.remove("src/{{ cookiecutter.code_directory }}/settings.py")

if not use_local_data_dir:
    os.remove("data")

if not create_example_files:
    os.remove("src/{{ cookiecutter.code_directory }}/pipeline_example.py")
    os.remove(
        "src/{{ cookiecutter.code_directory }}/preprocess_util_lib_example.py"
    )
    os.remove("notebooks/Test.ipynb")

if not keep_bsd3:
    os.remove("LICENSE")
else:
    # change the year to current
    new_text_lines = []
    with open("LICENSE", "r") as f:
        old_text_lines = f.readlines()
    for line in old_text_lines:
        if "YEAR" in line:
            line = line.replace("YEAR", str(datetime.today().year), 1)
        new_text_lines.append(line)
    with open("LICENSE", "w") as f:
        f.writelines(new_text_lines)

if not use_annotations:
    # remove annotation line
    new_text_lines = []
    with open("pyproject.toml", "r") as f:
        old_text_lines = f.readlines()
    for line in old_text_lines:
        if "ANN" in line:
            line = ""
        new_text_lines.append(line)
    with open("pyproject.toml", "w") as f:
        f.writelines(new_text_lines)