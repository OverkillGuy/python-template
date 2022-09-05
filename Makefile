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

try:
	-rm -rf template_expanded
	cookiecutter .   --no-input --output-dir template_expanded
	cd template_expanded/my-lovely-project && make
