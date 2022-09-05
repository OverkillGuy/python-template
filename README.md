# Python project skeleton

A project skeleton for Python projects.

> fill in your project name, description, and Python version, and you get a project!

Template built out of code repeated at least thrice by Jb.

## Usage

### On the command line

Install [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/) on your system:

	brew install cookiecutter  # system-wide
	pip install cookiecutter  # in your local virtualenv for separation

Try out the template:

	cookiecutter git@github.com:OverkillGuy/python-skeleton.git

It will then ask questions like python version and project name.

## Testing

This template has tests that ensure that we can render it (no stray
variables) as well as tests for the generated project ("can we
actually build the project?")

Use the convenient Makefile for testing:

	make      # defaults to target "all"
	make all  # equivalent
