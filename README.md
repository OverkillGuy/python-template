# Python project skeleton

A project skeleton for Python projects.

> fill in your project name, description, and Python version, and you get a project!

Template built out of code repeated at least thrice by Jb.

## Usage
## Usage

Use the `cookiecutter` templating command.

### Installing Cookiecutter

To install `cookiecutter`, consider using [pipx](https://pypa.github.io/pipx/)
to isolate the executable from your system:

	pipx install cookiecutter
	# Inject the dependencies used in this particular template
	pipx inject cookiecutter jinja2-git

Otherwise install it normally via pip, though we encourage you use a virtual
environment:

	pip install cookiecutter jinja2-git

### Using the template

Point the cookiecutter command to this repository to use it. This can be done by
using the locally cloned version of it, or if uploaded to Github, directly via
repo URL:

	# Assuming the python_skeleton lives at ~/git/python_skeleton
	cookiecutter ~/git/python_skeleton

It will then ask questions like python version and project name to get a fresh
repository, ready for action!

## Testing

This template has tests that ensure that we can render it (no stray
variables) as well as tests for the generated project ("can we
actually build the project?")

Use the convenient Makefile for testing:

	make      # defaults to target "all"
	make all  # equivalent

A target called `make try` with optional parameters `PYTHON_VERSION` and
`MAKE_TGT` is available to see the template expanded locally, running inside the
templated repo the make target defined by `MAKE_TGT`:

	make try  # defaults to PYTHON_VERSION=3.9 MAKE_TGT=all
	# You can override these variables:
	make try PYTHON_VERSION=3.10
	make try MAKE_TGT=docker-build  # to run make docker-build inside repo

## TODO list

- Fix non-unique docker image name causing clashes during parallel tests
- Optimize Dockerfile.release to copy pre-built wheel file
- App-or-library binary choice with Poetry.lock
- Add optional file creation system (files with big IF vars, and if to be
  deleted, have a unique content in it like `DELETETHISFILE`, with post-hook
  deleting files matching that content)
- Add a DESIGN.md to document big architectural decisions
  - Create (Sphinx) docs for the template?
