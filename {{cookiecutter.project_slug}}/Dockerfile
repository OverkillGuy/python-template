FROM python:{{ cookiecutter.python_version}}

# Bring poetry, our package manager, and pre-commit hooks
RUN pip install poetry pre-commit

# Workaround critical-level CVEs in Python image
# By forcing just security update (no feature-full updates, as part of apt conf)
RUN apt-get update && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /workdir
WORKDIR /workdir

RUN poetry install
