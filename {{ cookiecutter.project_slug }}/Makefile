# Define constants

# general
mkfile_path := $(abspath $(firstword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
current_abs_path := $(subst Makefile,,$(mkfile_path))

# pipeline constants
# PROJECT_NAME
pipeline_image_name := "{{ cookiecutter.project_slug }}-pipeline"
pipeline_container_name := "{{ cookiecutter.project_slug }}-pipeline-container"
pipeline_dir := "$(current_abs_path){{ cookiecutter.code_directory }}"

# notebook constants
notebooks_image_name := "{{ cookiecutter.project_slug }}-notebooks"
notebooks_container_name := "{{ cookiecutter.project_slug }}-notebooks-container"
notebooks_dir := "$(current_abs_path)notebooks"

# environment variables
# include .env

{% if cookiecutter.docker == "yes" %}# Build Docker image for pipeline
build-pipeline:
	docker build -t $(pipeline_image_name) -f "${pipeline_dir}/Dockerfile" $(current_abs_path) --target prod

# Run pipeline image
run-pipeline:
	docker run -v $(current_abs_path)data:/{{ cookiecutter.project_slug }}/data -v $(current_abs_path)output:/{{ cookiecutter.project_slug }}/output $(pipeline_image_name) 

run-pipeline-bash:
	docker run -it -v $(current_abs_path)data:/{{ cookiecutter.project_slug }}/data -v $(current_abs_path)output:/{{ cookiecutter.project_slug }}/output $(pipeline_image_name) /bin/bash

# Build Docker image for notebooks
build-notebooks:
	docker build -t $(notebooks_image_name) -f "${notebooks_dir}/Dockerfile" $(current_abs_path)

run-notebooks:
	docker run -v $(current_abs_path)data:/{{ cookiecutter.project_slug }}/data \
	-v $(notebooks_dir)/:/{{ cookiecutter.project_slug }}/notebooks \
	-v $(current_abs_path)output:/{{ cookiecutter.project_slug }}/output \
	--name $(notebooks_container_name) --rm -p 8888:8888 -t $(notebooks_image_name) \
	jupyter lab --port=8888 --ip='*' --NotebookApp.token='' --NotebookApp.password='' \
	--no-browser --notebook-dir=/{{ cookiecutter.project_slug }}/notebooks --allow-root
{% endif %}{% if cookiecutter.cluster == "yes" %}
open-ssh-login-node:
	code --remote ssh-remote+fe.ds ~/{{ cookiecutter.project_slugj }}
{% endif %}