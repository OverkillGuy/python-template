# Run 'make help' to see guidance on usage of this Makefile

## Default command, run via 'make' or 'make all'
.PHONY: all
all: install lint test build install-hooks

## Generate the help message by reading the Makefile
.PHONY: help
help:
	@echo "This makefile contains the following targets, from most commonly used to least: (docs first, then target name)"
	@awk \
		'/^##/ {sub(/## */,""); print} \
		/^[a-z0-9-]+:/ && !/.PHONY:/ \
			{sub(/:.*/, ""); print "⮡   \033[31;1;4m" $$0 "\033[0m\n" }' \
		Makefile

## Set up the virtualenv and install the package + dependencies
.PHONY: install
install:
	uv sync

## Run the linters and formatters on all files (not just staged for commit)
.PHONY: lint
lint:
	pre-commit run --all --all-files

## Run the simplest test, in one place
TEST_VARIANT="run_func=run_native-python_version=3.13"
.PHONY: test
test:
	uv run pytest \
		"tests/test_template.py::tests_template_makes_ok[${TEST_VARIANT}]"

## Runs ALL tests, slow (~10mins) (matrix-ing python version x test case)
slow-test:
	uv run pytest tests/

## Build the tarball package
## (Wheel won't include template path)
.PHONY: build
build:
	uv build --sdist

## Expands the template in a local folder, for experimenting
## see variables PYTHON_VERSION, MAKE_TGT, REF
.PHONY: try
PYTHON_VERSION=3.13
MAKE_TGT=all
# MAKE_TGT=docker-build docker-build-release
RANDOMIZED_PROJECT_NAME=$(shell uv run python -c 'import faker_microservice;from faker import Faker;fake = Faker();fake.add_provider(faker_microservice.Provider);print(fake.microservice().replace("-", " ").replace("_", " ").capitalize())')
ARGS?=
REF=HEAD
TGTDIR=../template_expanded
try:
# Wipe previous such templating if any
	-rm -rf ${TGTDIR}
# Re-expand with randomized vars
	uv run copier copy \
		. \
		${TGTDIR} \
		--vcs-ref ${REF} \
		--defaults \
		--UNSAFE \
		-d "description=A cool project" \
		-d "python_version=${PYTHON_VERSION}" \
		-d "project_name=${RANDOMIZED_PROJECT_NAME}" ${ARGS}
# Get in there and run make
	cd ${TGTDIR} \
		&& make ${MAKE_TGT}

## Run an attempt at 'copier update' of the template-expanded repo
## Perfect to test changes to template. ONLY WORKS FOR COMMITED CHANGES
## Edit ARGS var to give copier flags
.PHONY: try-update
try-update:
	uv run copier update \
		--conflict inline \
		${TGTDIR} ${ARGS}

## Update the python gitignore file from upstream online
.PHONY: python-gitignore
python-gitignore:
	wget -O data/Python.gitignore \
		https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore

## Set up the pre-commit hooks to execute on next git commit
.PHONY: install-hooks
install-hooks:
	pre-commit install

##  Make a release commit + tag, creating Changelog entry
##  Set BUMP variable to any of uv-supported (major, minor, patch...)
##  Default the bump to a patch (v1.2.3 -> v1.2.4)
BUMP=patch
.PHONY: release
release:
# Set the new version Makefile variable after the version bump
	$(eval NEW_VERSION := $(shell uv version --short --bump ${BUMP}))
	$(eval TMP_CHANGELOG := $(shell mktemp))
	@sed \
		"s;\(## \[Unreleased\]\);\1\n\n## v${NEW_VERSION} - $(shell date +%Y-%m-%d);" \
		CHANGELOG.md > ${TMP_CHANGELOG}
	@mv --force ${TMP_CHANGELOG} CHANGELOG.md
	uv lock
	git add CHANGELOG.md pyproject.toml uv.lock
	git commit -m "Bump to version v${NEW_VERSION}"
	git tag --annotate "v${NEW_VERSION}" \
		--message "Release v${NEW_VERSION}"

##  Less commonly used commands

##  Generate/update the uv.lock file
.PHONY: lock
lock:
	uv lock

##  Update dependencies (within pyproject.toml specs)
##  Update the lock-file at the same time
.PHONY: update
update:
	uv lock --upgrade


## Install tools (uv, pre-commit) via pipx
## Assumes you have pipx installed
# See https://jiby.tech/post/my-python-toolbox/#pipx-for-cli-installs-not-pip
.PHONY: install-tools
install-tools:
	uv self version
	uv tool install pre-commit

## Delete the virtualenv to clean dependencies
## Useful when switching to a branch with less dependencies
.PHONY: venv-nuke
venv-nuke:
	find .venv -delete
