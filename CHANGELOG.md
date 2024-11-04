# Changelog for the python-template

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
The project uses semantic versioning (see [semver](https://semver.org)), though
templating versions are not perfect matches for semantic versions.

## [Unreleased]

### Fixed

- Simplified `package_name` variable, removed the need to run `context.py` to
  generate it. This should mean no need for unsafe calls
- Properly ignore test folders from coverage measurement

## v1.7.1 - 2024-10-27

## Fixed

- Fixed mismatching `poetry` version in `release.Dockerfile` to match main
  `Dockerfile`.

## v1.7.0 - 2024-10-26

### Added

- Updated pre-commit hook versions

### Fixed

- No more duplicate label warnings during `make docs`. Done by removing the
  (old) autodoc and using (new) autodoc2 exclusively, resolving the clash.
- Typo in use of `dynamic_versioning` inside `pyproject.toml` causing
  `dynamic_versioning=True` to be ignored, effectively set as if
  `dynamic_versioning=False`.
- Ruff TOML config in pre-commit now set properly

### Changed

- `package_name` variable is now derived from a python script. No functional
  change in the template, just how the value was computed.

## v1.6.0 - 2024-05-07

### Added

- New parameter `dynamic_version`, defaulting to `True`. Enable to use proximity
  to a git tag as package version. On git tags, package version is tag. On
  non-tagged commits, version is last tag + number of commits as post. Uses
  `poetry-dynamic-versioning`, using `dunamai` library
- New `make help` shows command help in repo
- `Makefile` now loads `.env` contents as variables, if file exists
- Python 3.12 now supported, default version of the template
- Updated pre-commit hook versions

### Fixed

- Remove astroid pinning from v1.4.0, upstream updated, no longer breaks
- Test file name no longer mangled by templating engine (as `tests/test_.py`)
- Markdownlint pre-commit hook no longer fails with "punycode dependency warn"

## v1.5.0 - 2024-01-26

### Changed

- No longer asking `package_name` as question with a default that's
  overrideable, now derived from `project_name` (converted to
  lowercase_with_underscore) without asking, as it was always intended.

### Added

- Allow setting a container registry when building. Run `make
  DOCKER_REGISTRY=docker.io/example/ docker-build-release` to automatically tag
  the image with a specific registry.
- Gitignore's "Python files" section is now auto-fetched from latest
  Github/gitignore repo, see `make python-gitignore`.
- Git/docker ignore files are now shared via jinja templating, clearly
  delineated from the rest of the file (which can be edited by hand afterwards)

### Fixed

- Project name validator now allows more than lowercase characters (validating
  regex now `^[A-Z0-9].+$` instead of old `^[A-Z][a-zA-Z0-9\' ]+$`).
- `make release` now uses annotated git tags instead of lightweight tags (per
  `man git-tag(1)`, non-annotated tags are for "private or temporary object
  labels", and won't show up in `git describe` by default).
- `make release` now more portable (previously relied on GNU date and GNU sed)
- Git/docker ignore files now properly ignore text editor swap/backup files.
- Docker context (cache) no longer gets invalidated due to git operations.

### Removed

- Internal `make lint` no longer runs `poetry-lock` hook, useless for a
  template-oriented `pyproject.toml`. No change for template users!

## v1.4.0 - 2023-10-06

### Added

- Release-oriented Dockerfile now uses the `poetry.lock` contents as deps.
  Via new impl of `make export-requirements`, copied into image.
- New `make check-requirements`, verifies `requirements.txt` == `poetry.lock`.
- Release-oriented dockerfile uses built CLI as entrypoint.
  Can now run `docker run {{ project-slug }}:0.1.0 --help`.

### Fixed

- `make docs` no longer crashes with exception: 'Module' object has no
  attribute 'doc'. Dep astroid v3.0.0 is breaking, pinned for the moment.

## v1.3.1 - 2023-09-05

### Fixed

- Replaced `docs/source/index.rst` to `index.md`. Docs all Markdown via myst.

### Removed

- Unnecessary file `.flake8` removed, not needed since move to `ruff`

## v1.3.0 - 2023-08-29

### Added

- New pre-commit hook `poetry-check` and `poetry-lock`, validating poetry setup
- Update `Dockerfile`, used as base dev image
  - Debian version bookworm
  - `poetry` to `1.6.1`
  - `pre-commit` to `3.3.3`
- New project-name validator rules, enforcing 'Capitalized With Spaces' rule

### Fixed

- `make lock` no longer updates dependencies, via `--no-update` flag.

### Removed

- `yamllint` pre-commit hook: yaml _validator_ already packed in default hooks,
  no need for yaml pretty-printer!

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
