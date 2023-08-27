# Changelog for the python-template

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
The project uses semantic versioning (see [semver](https://semver.org)), though
templating versions are not perfect matches for semantic versions.

## [Unreleased]

### Added

- New pre-commit hook `poetry-check` and `poetry-lock`, validating poetry setup
- Update `Dockerfile`, used as base dev image
  - Debian version bookworm
  - `poetry` to `1.6.1`
  - `pre-commit` to `3.3.3`
- New project-name validator rules, enforcing 'Capitalized With Spaces' rule

### Removed

- `yamllint` pre-commit hook: yaml validator already packed in default hooks, no
  need for yaml pretty-printer


## v1.2.0 - 2023-08-24

### Added

- Explicit choice of "Google" docstring style

### Fixed

- Git repo initialization feature restored via `_tasks`
- `make build` now builds sdists (`source.tar.gz`) as well as bdist (wheels,
  binary package). This fixes `poetry publish` after `make (build)` uploading
  only a binary package without source
- `ruff` linter no longer yells about pydocstyle rules

## v1.1.0 - 2023-06-07

### Added

- Faster linting via `ruff`, replacing `flake8` and `isort` pre-commit hooks
- Dash/Zeal docsets are now generated in `docs/build/docset` via `make docs`
- Markdown support in python docstrings, via
  [myst-parser](myst-parser.readthedocs.io/) and [sphinx-autodoc2](https://sphinx-autodoc2.readthedocs.io/en/latest/quickstart.html#using-markdown-myst-docstrings)

### Fixed

- Template self-tests now refer properly to current `HEAD` commit, not last tagged
- Fix pytest warnings via update of `pytest-coverage` to `4.*`

## v1.0.0 - 2023-05-02

### Added

- New python template using `copier>=7.1.0`, validated by tests and
  teaching/explaining itself via design document.
