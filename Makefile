all: install format test build

install:
	poetry install

format:
	poetry run isort tests/
	poetry run black tests/

test:
	poetry run pytest tests/

build:
	poetry build

PYTHON_VERSION=3.8
MAKE_TGT=docker-build docker-build-release
try:
	-rm -rf template_expanded
	cookiecutter \
		--no-input \
		--output-dir template_expanded \
		. \
		'python_version=${PYTHON_VERSION}'
	cd template_expanded/my-lovely-project && make ${MAKE_TGT}
