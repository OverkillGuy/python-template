FROM python:{{ cookiecutter.python_version }} as builder

# Bring poetry, our package manager
ARG POETRY_VERSION=1.2.0
RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

# Copy code in to build a package
COPY . /workdir/
WORKDIR /workdir

RUN poetry build -f wheel

# Start over with just the binary package install
FROM python:{{ cookiecutter.python_version }}-slim as runner

COPY --from=builder /workdir/dist /app

RUN pip install --no-cache-dir /app/*.whl
