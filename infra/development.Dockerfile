FROM python:3.9-slim-bullseye
ENV DIR=project
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ python3-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /${DIR}
COPY requirements.txt /${DIR}/requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN apt-get update
COPY setup.py /${DIR}
RUN pip install -e .
