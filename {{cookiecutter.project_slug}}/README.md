# {{cookiecutter.project_name}}

{{cookiecutter.description}}

Requires Python {{cookiecutter.python_version}}


## Usage

Depends on what the code in there does.


## Development

### Python setup

This repository uses Python{{ cookiecutter.python_version }}, using
[Poetry](https://python-poetry.org) as package manager to define a
Python package inside `src/{{cookiecutter.package_name}}/`.

`poetry` will create virtual environments if needed, fetch
dependencies, and install them for development.


For ease of development, a `Makefile` is provided, use it like this:

	make  # equivalent to "make all" = install lint test build
	# run only specific tasks:
	make install
	make lint
	make test
	# Combine tasks:
	make install test

Once installed, the module's code can now be reached through running
Python in Poetry:

	$ poetry run python
	>>> import {{cookiecutter.package_name}}
	>>> print({{cookiecutter.package_name}}.version)
	"0.1.0"

This codebase uses [pre-commit](https://pre-commit.com) to run linting
tools like `flake8`. Use `pre-commit install` to install git
pre-commit hooks to force running these checks before any code can be
committed, use `make lint` to run these manually. Testing is provided
by `pytest` separately in `make test`.
