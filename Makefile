all: install format test build

install:
	poetry install

format:
	poetry run isort tests/
	poetry run black tests/

# Run a (fast, native) test suite which covers most test cases
# See also: make slow-test, make slow-test-parallel, make try
TEST_VARIANT1="mode=just_a_CLI-python_version=3.10-runfunc=run_native"
TEST_VARIANT2="mode=REST_API_client-python_version=3.10-runfunc=run_native"
test:
	poetry run pytest \
		"tests/test_template.py::tests_template_makes_ok[${TEST_VARIANT1}]" \
		"tests/test_template.py::tests_template_makes_ok[${TEST_VARIANT2}]"

# Runs ALL tests, slow (~30mins) (matrix-ing python version x test case x native-or-dockerized)
slow-test:
	poetry run pytest

# Run ALL tests but a few at a time (<10min). Adjust WORKERS to ~CPU count
WORKERS=4
slow-test-parallel:
	poetry run pytest tests/ --workers ${WORKERS}

build:
	poetry build

# Expands the template in a local folder, for experimenting
PYTHON_VERSION=3.10
MAKE_TGT=all
# MAKE_TGT=docker-build docker-build-release
RANDOMIZED_PROJECT_NAME=$(shell poetry run python -c 'import faker_microservice;from faker import Faker;fake = Faker();fake.add_provider(faker_microservice.Provider);print(fake.microservice().replace("-", " ").replace("_", " ").capitalize())')
try:
# Wipe previous such templating if any
	-rm -rf template_expanded
# Re-expand with randomized vars
	cookiecutter \
		--no-input \
		--output-dir template_expanded \
		. \
		'python_version=${PYTHON_VERSION}' 'project_name=${RANDOMIZED_PROJECT_NAME}'
# Get in there and run make
	cd template_expanded/ \
		&& cd * \
		&& make ${MAKE_TGT}
