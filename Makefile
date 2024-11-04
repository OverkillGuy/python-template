all: install lint test build

install:
	poetry install

lint:
	pre-commit run --all

# Run a (fast, native) test suite which covers most test cases
# See also: make slow-test, make slow-test-parallel, make try
TEST_VARIANT="python_version=3.10-runfunc=run_native"
test:
	poetry run pytest \
		"tests/test_template.py::tests_template_makes_ok[${TEST_VARIANT}]"

# Runs ALL tests, slow (~30mins) (matrix-ing python version x test case x native-or-dockerized)
slow-test:
	poetry run pytest tests/

# Run ALL tests but a few at a time (<10min). Adjust WORKERS to ~CPU count
WORKERS=4
slow-test-parallel:
	poetry run pytest tests/ --workers ${WORKERS}

build:
	poetry build

.PHONY: try
# Expands the template in a local folder, for experimenting
PYTHON_VERSION=3.12
MAKE_TGT=all
# MAKE_TGT=docker-build docker-build-release
RANDOMIZED_PROJECT_NAME=$(shell poetry run python -c 'import faker_microservice;from faker import Faker;fake = Faker();fake.add_provider(faker_microservice.Provider);print(fake.microservice().replace("-", " ").replace("_", " ").capitalize())')
DYN_VERSION=True
ARGS?=
try:
# Wipe previous such templating if any
	-rm -rf template_expanded
# Re-expand with randomized vars
	poetry run copier copy \
		. \
		'template_expanded/new_project/' \
		--vcs-ref HEAD \
		--defaults \
		--UNSAFE \
		-d "description=A cool project" \
		-d "python_version=${PYTHON_VERSION}" \
		-d "dynamic_version=${DYN_VERSION}" \
		-d "project_name=${RANDOMIZED_PROJECT_NAME}" ${ARGS}
# Get in there and run make
	cd template_expanded/ \
		&& cd * \
		&& make ${MAKE_TGT}

.PHONY: try-update
try-update:
	poetry run copier update \
		--conflict inline \
		'template_expanded/new_project/'

.PHONY: python-gitignore
python-gitignore:
	wget -O data/Python.gitignore \
		https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore

# Make a release commit + tag, creating Changelog entry
# Set BUMP variable to any of poetry-supported (major, minor, patch)
# or number (1.2.3 etc), see 'poetry version' docs for details
.PHONY: release
# Default the bump to a patch (v1.2.3 -> v1.2.4)
release: BUMP=patch
release:
# Set the new version Makefile variable after the version bump
	$(eval NEW_VERSION := $(shell poetry version --short ${BUMP}))
	$(eval TMP_CHANGELOG := $(shell mktemp))
	sed \
		"s/\(## \[Unreleased\]\)/\1\n\n## v${NEW_VERSION} - $(shell date +%Y-%m-%d)/" \
		CHANGELOG.md > ${TMP_CHANGELOG}
	mv --force ${TMP_CHANGELOG} CHANGELOG.md
	git add CHANGELOG.md pyproject.toml
	git commit -m "Bump to version v${NEW_VERSION}"
	git tag --annotate "v${NEW_VERSION}" \
		--message "Release v${NEW_VERSION}"
