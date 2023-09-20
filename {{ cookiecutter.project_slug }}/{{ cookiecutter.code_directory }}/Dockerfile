FROM python:3.11-bookworm as devcontainer
ENV DIR={{ cookiecutter.project_slug }}
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ python3-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /${DIR}
COPY requirements.txt /${DIR}/requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN apt-get update
COPY setup.py /${DIR}
RUN pip install -e .

FROM devcontainer as prod

COPY {{ cookiecutter.code_directory }} ./{{ cookiecutter.code_directory }}
COPY config ./config

CMD ["python", "{{ cookiecutter.code_directory }}/main.py"]