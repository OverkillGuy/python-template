# My Python template

An opinionated template for new Python projects

> Fill in your project name, description, and Python version, and you get a project!

Template built out of code repeated at least thrice, distilling years of practice.

## Usage

Use the `copier` templating command.
Read up on the template's design decisions in the [DESIGN.md](./DESIGN.md) file.

### Installing Copier

To install `copier`, consider using [pipx](https://pypa.github.io/pipx/)
to isolate the executable from your system:

```shell
pipx install copier
```

Otherwise install it normally via pip, though we encourage you use a virtual
environment:

```shell
pip install copier
```

### Using the template

Run copier with a URL to this repository. This can be done by cloning the
repository, or directly via repository URL on Github:

```shell
copier copy --trust gh:OverkillGuy/python-template TARGET_DIR
```

It will then ask questions like python version and project name to get a fresh
repository, ready for action!

## Testing

This template has tests that ensure that we can render it (no stray
variables) as well as tests for the generated project ("can we
actually build the project?")

Use the convenient Makefile for testing:

```shell
make      # defaults to target "all"
make all  # equivalent
```

A target called `make try` with optional parameters `PYTHON_VERSION` and
`MAKE_TGT` is available to see the template expanded locally, running inside the
templated repository the make target defined by `MAKE_TGT`:

```shell
make try  # defaults to PYTHON_VERSION=3.10 MAKE_TGT=all
# You can override these variables:
make try PYTHON_VERSION=3.11
make try MAKE_TGT=docker-build  # to run make docker-build inside repository
```
