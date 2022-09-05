FROM python:{{ cookiecutter.python_version}}

# Bring poetry, our package manager, and pre-commit hooks
ARG POETRY_VERSION=1.2.0
ARG PRECOMMIT_VERSION=2.20.0
RUN pip install --no-cache-dir \
    poetry==${POETRY_VERSION} \
    pre-commit==${PRECOMMIT_VERSION}

# Already in docker, no venv needed
ENV POETRY_VIRTUALENVS_CREATE=false


# Workaround critical-level CVEs in Python image
# By forcing just security update (no feature-full updates, as part of apt conf)
RUN apt-get update && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /workdir
WORKDIR /workdir

# Install the local package dependencies (dev-mode)
RUN poetry install
