# Pull base Docker image
# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/selecting.html#jupyter-scipy-notebook
FROM jupyter/minimal-notebook:python-3.11

ENV DIR={{ cookiecutter.project_slug }}
# Create working directory
WORKDIR /${DIR}

# Install Python 3 packages
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Installing our code as a package
COPY setup.py .
COPY {{ cookiecutter.code_directory }} ./{{ cookiecutter.code_directory }}
RUN pip install -e .

# Copy notebooks folder
COPY notebooks ./notebooks