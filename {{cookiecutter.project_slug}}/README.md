# {{cookiecutter.project_name}}

{{cookiecutter.description}}

Requires Python {{cookiecutter.python_version}}

## Usage

Depends on what the code in there does.

### Run the command

Install the module first:

```shell
make install
# or
poetry install
```

Then inside the virtual environment, launch the command:

```shell
# Run single command inside virtualenv
poetry run {{ cookiecutter.project_slug }}

# or
# Load the virtualenv first
poetry shell
# Then launch the command, staying in virtualenv
{{ cookiecutter.project_slug }}
```

## Development

### Python setup

This repository uses Python{{ cookiecutter.python_version }}, using
[Poetry](https://python-poetry.org) as package manager to define a
Python package inside `src/{{cookiecutter.package_name}}/`.

`poetry` will create virtual environments if needed, fetch
dependencies, and install them for development.

For ease of development, a `Makefile` is provided, use it like this:

```shell
make  # equivalent to "make all" = install lint docs test build
# run only specific tasks:
make install
make lint
make test
# Combine tasks:
make install test
```

Once installed, the module's code can now be reached through running
Python in Poetry:

```shell
$ poetry run python
>>> from {{cookiecutter.package_name}} import main
>>> main("blabla")
```

This codebase uses [pre-commit](https://pre-commit.com) to run linting
tools like `flake8`. Use `pre-commit install` to install git
pre-commit hooks to force running these checks before any code can be
committed, use `make lint` to run these manually. Testing is provided
by `pytest` separately in `make test`.

### Documentation

Documentation is generated via [Sphinx](https://www.sphinx-doc.org/en/master/),
using the cool [myst_parser](https://myst-parser.readthedocs.io/en/latest/)
plugin to support Markdown files like this one.

Other Sphinx plugins provide extra documentation features, like the recent
[AutoAPI](https://sphinx-autoapi.readthedocs.io/en/latest/index.html) to
generate API reference without headaches.

To build the documentation, run

```shell
# Requires the project dependencies provided by "make install"
make docs
# Generates docs/build/html/
```

To browse the web version of the documentation you just built, run:

```shell
make docs-serve
```

And remember that `make` supports multiple targets, so you can generate the
documentation and serve it:

```shell
make docs docs-serve
```

### Templated repository

This repository was created by the cookiecutter template available at
<{{ cookiecutter.template_url }}>,
using commit hash: `{% gitcommit %}`.
