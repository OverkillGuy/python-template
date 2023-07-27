# Template design

A discussion of the template of this repo, explaining the design choices that
make up its content.

## Template system decisions

### copier, goodbye cookiecutter

Cookiecutter is the package got us all in the templating business.
But it's frozen in time, missing many features.

Instead, we use [copier](https://copier.readthedocs.io/en/latest/).

Copier can do what cookiecutter can, but by baking in the template answers in
file, it enables project lifecycle, backporting the updates to template to
generated code. Copier also contains many other features like conditional file
inclusion, which were gripes of cookiecutter.

## Language-agnostic design choices

Aspects that aren't related to the template being a Python one.

### README.md structure

Every repo needs a README file to explain the most basic things about it:

- What is this?
- What is it built with? (major dependencies)
- How does one install/use it?
- How does one test it/extend it?

### Makefile

Both to simplify the common commands via automation (aliases), and to document
these actions, explaining to others how the system is built/run.

Aim to document the 80% of very common build commands, as well as a further 10%
of "seldom used but critical commands to know". Avoid very complex commands or
complicated compositions of actions that force reader to learn complex Makefile
commands.

### Pre-commit

Use the tool [pre-commit](https://pre-commit.com) to enforce some local rules
like no mixing spaces and tabs in the same file, no merge conflict may be
committed, etc.

Enforcing these as pre-commit steps guarantees a sort of "mini-CI" without a
server, which is handy.

On the other hand, these are blocking commits until completion, so complex
commands, that run for tens of seconds, like running full tests, is a bad idea,
as you need your pre-commit hooks to stay snappy.

Use the pre-commit hooks for language-specific linters and formatters too, as
well as a few other useful generic hooks to run (such as `shellcheck` for
maintaining some semblance of correctness in shell scripts).

To make sure that everyone does run the pre-commit hooks without thinking about
it, the hooks are automatically installed as part of running the default `make`
command.

### CHANGELOG.md

We write down the release notes of the project using a change log.
As the saying goes, "friends don't let friends use `git log` as changelog".

Format-wise, adopt the one and only
[keepachangelog.com](https://keepachangelog.com) format, which provides some
convenient guarantees for users.

We do NOT recommend conventional commits, and avoided using any
conventional-commits-based tooling for changelog generation. It is a belief
deeply held by the author that git commit messages should be detailed,
thoughtful messages. Conventional commits, by their push for automation, cause
developers to think LESS about commit messages, instead of more.
Nevertheless, nothing in the template prevents such tooling from filling in the
changelog file.

### Dockerfile

We first provide a "dev" `Dockerfile`, which is meant for working in the project,
including all tools and developer-only dependencies.
That file is useful to build code in CI, providing all tools required.

Separately from that rather heavy docker image, we provide a release-only
Dockerfile, called `release.Dockerfile`. This image has minimal footprint,
starting with the smallest possible base, and installing-in solely built
package, for release purposes. The naming convention assumes that "Dockerfile"
is a file suffix, which seems to align with Github conventions, as previous
attempts at naming something `Dockerfile.release` failed to syntax-highlight on
Github.

The choice to make the dev Dockerfile "main" (using the well-known name
`Dockerfile`) is because most developer activities done on the repository
require that dev image, as opposed to the "release" activity being a
single-purpose command, used in an activity that happens only rarely, late in
the development process.

A `.dockerignore` file (similar in purpose to `.gitignore` files but for docker
context) is provided, copying most of the `.gitignore` contents, except for the
`dist/` folder, which is allowed for copy, as it is where installable packages
are built by the language, for use by the release Dockerfile.

Use `hadolint` linter to cover Dockerfile best practices.

### Git-tag the initial commit

The intent of this template is to give what some call a "walking skeleton", a
ready to deploy though not very usefull app, with all the equipment we need to
start development.

In that sense, the template we deploy is a fully functional app, and as such,
can be deployed as-is either as python package (`make build`), or as a docker
image with the python package (`make docker-build-release`).

Because of this, we enforce the first commit of new repos, which is templated to
inform users of the source of the template (down to commit hash of template
used), to be tagged as `v0.1.0`.
This decision also happens to line up the `CHANGELOG.md` content, which insists
the current date is release of `v0.1.0`.

## Python-specific design choices

### Use of Poetry

As many have noted before, `pip` and `virtualenv` are absolutely sufficient to make
python code flow.
But having experienced other languages and their well-integrated tooling for
package creation, virtual environment management, build and release, `poetry` is
just too convenient.

It covers the package definition (much, much more simply than obscure
`setup.py`, with a well defined specification, and declaratively, avoiding
arbitrary code execution that `setup.py` somehow encourages).
It covers the virtual-environment management too. We recommend the setting
`virtualenvs.in-project` be set to `true` (see `make poetry-venv-local`), to
allow for easy inspection and wipe of the `.venv/` (see `make
poetry-venv-nuke`).

All in all, these features are too good to ignore, just wrap all commands in
`poetry run` to ensure venv is respected, and move on.

There is no well-known Docker image with `poetry` installed, so the first step
in that image is installing poetry itself. Note the release docker image does
not contain poetry, nor does it need it, only installing the built package via
`pip`, to minimize dependencies.

### Gitignore

The `.gitignore` file is taken from [Github's gitignore
project](https://github.com/github/gitignore), specifically the Python
language's gitignore.
This is a community standard for what files are worth ignoring for version
control purposes in each language/editor.

To make tracking of that copied `.gitignore`, the Github source is linked in
comments, up to the specific commit hash that gave the content.

Only one line was changed: the `poetry.lock` file, which was marked as tracked,
from its default of untracked. The reasoning is that only apps should lock their
dependencies for reproducibility, with libraries supposed to allow ranges of
dependencies being used, as decided best by library users. Given the template is
meant to build a ready-for-use CLI app, the library usecase is out the window by
default, and we should instead ask users to actively re-ignore the lockfile,
instead of disabling reproducibility by default for those who need it.

### Use Src folder for holding python package contents

There are many reasons to use an `src/` folder for holding Python package
source.

The simplest one is just to separate where the source code is clearly,
regardless of the package name. When the package is called for instance
`docker-tools`, it's easy for that folder name to blend in with the rest of the
top-level folder. When more than one package is declared in a single repo, this
single `src/` folder keeps things tidy.

Beyond that, use of `src/` folder, in conjunction with having most tests in a
separate `tests/` folder (rather than encouraging tests inside the package, like
`src/PACKAGENAME/tests/`), force the devs to use proper full-name imports rather
than allowing relative imports like `from .. import xyz`.

And finally, the most technical reason is the one defined in [Testing &
packaging](https://hynek.me/articles/testing-packaging/):
> If you use the "ad hoc" layout without an `src/` directory, *your tests do not
> run against the package as it will be installed by its users*. They run
> against whatever the situation in your project directory is.

### Use latest Python available as default

Since this template is meant for me to build for future work, I have no reason to
allow older versions of Python to be used in new project.

### Formatters

Formatters avoids asking the question of code format. Black, the formatter, is a
fantastic tool, and is opinionated, as its tagline shows:
> You can choose any color. As long as it is black.

While 79 lines, per PEP8, is the default choice for anything else, black's 88
characters is fine enough, and not worth changing.

To complement formatting, we use import sorters to group stdlib vs first vs
third party imports, see "Linters" section below for how.

For docstrings style, we prefer Google's style to NumPy's, for readability
purposes. See [a visual comparison of the two
styles](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/index.html#google-vs-numpy).
When docstrings are parsed by documentation tooling (see dedicated
"Documentation" section), these docstring conventions turn pretty text files
into wonderful documentation pages.

### Linters

Every language has a few gotchas, or untidy practices. To counter that, we have
linters, to warn/fix if possible.

We recommend the brand new mega-linter `ruff`, which is ridiculously fast, and
replaces all of previous `flake8`, `pylint`, `isort`, and most of the popular
flake8 extensions. This single package also avoids having to pin and update many
packages.

Note that ruff is still quite new on the Python scene, and may seem to lack
complex features, but its very fast development speed has taken by storm the
Python world.

As Tiangolo (FastAPI creator) says:
> Ruff is so fast that sometimes I add an intentional bug in the code just to
> confirm it's actually running and checking the code.

### Use of typing

I like the Python type hints, and they're well supported. So we use typing where
we can.

Mark the package as typed for downstream users via presence of `py.typed` empty
file.

Use `mypy` to enforce all that typing. It works.

### Pre-commit hooks for linting and formatting

All the linters and formatters could be part of the dev-dependencies of the
package, but it's even nicer to keep all of these as pre-commit checks,
enforcing them before committing.

This does mean a zero tolerance policy on linter issues, which is pretty harsh.
But, as with many warnings, the moment we let one warning creep in the build, we
have 100, and warnings become meaningless.

### Default app is a CLI app

Most of what the template author finds themselves doing is Python command line
tools, or at least library code with a command line entrypoint as fallback.

Using `argparse` (solid tool, not worth bringing a new package over for
`click`), define a basic CLI interface to prepare for whatever function we'll
build.

### Default app is a HTTP API client

Beyond building "mostly a CLI app", the author found it necessary to repeat a
few times the same code for importing an HTTP client library, parsing some kind
of secret token from file or envvar, and hitting an API with it, with tests that
mock such a request.

Make the very most default app such an HTTP API client, keeping the CLI
entrypoint for convenience.

For users not wanting the full HTTP API client, the alternative is "just" a CLI
with no HTTP dependency.

### Test everything

Default app has tests for the CLI under use, to prove the CLI can be invoked,
and that the arguments given make sense. For the HTTP API client, we also test
separately that the main entrypoint hits the (mocked) requested endpoint.

### Documentation

Every project worth writing about is worth documenting.

Use Sphinxdocs for documentation, as it is more flexible and have more
integrations than more recent tools like `mkdocs`).
But ReStructuredText is kind of a nightmare, so we integrate the fantastic
`myst_parser` to enable Markdown.

The theme is the famous ReadTheDocs one, a good enough default for most
projects.

We include the README and CHANGELOG files (pulled from the top-level of the
project) as first of the docs, to get devs going.

For documentation of the code itself, we lean on the recent `sphinx-autodoc2` to
include the code's API reference, in particular for its support of markdown
docstrings.

Docs are only useful if read. One of the most convenient way to consume
developer documentation is Dash/Zeal "docsets", a derivative of HTML docs,
pre-indexed by keyword, for offline use. We use `doc2dash` to automatically
build such docsets via `make docs`, generating a folder under
`docs/build/docset/`, ready for copy into your local docset tooling.

### Release Dockerfile force-rebuilds package

The Dockerfile for release is a standalone Dockerfile that force-rebuilds the
binary package of the app, instead of using (via `COPY`) a wheel file built via
`make build` beforehand.

This is chosen because it allows self-contained (hermetic) builds of the
released image, where we don't assume any available poetry dependency to build
the wheel file itself.

This decision is backtracking from a previous iteration of the template, where
the package was assumed already built via `make build`, and COPY-ed in. The
change of opinion came when adding support for Python 3.11, when the local
python version on dev machine (3.10) wasn't able to build the package being
tested (=3.11), contradicting the belief held beforehand that `poetry build` is
a reliable command that always works, even with a difference of environments
between template-target and local devenv. Combined with the need to change the
`.dockerignore` (which was unpalatable already), the need for hermetic build
pushed to reverse the decision and use self-contained docker build, even if it
means being back to multi-stage builds.
