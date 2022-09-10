import os
import subprocess

import pytest
from cookiecutter import main as ck
from cookiecutter.generate import generate_context
from cookiecutter.prompt import prompt_for_config
from pytest_cases import parametrize_with_cases

# The config in cookiecutter.json, once expanded
DEFAULT_CONF = prompt_for_config(generate_context(), no_input=True)

# TODO: Use pytest-cases to parametrize out the python_version etc
@pytest.fixture
def template(tmp_path):
    """Invokes cookiecutter simply without specific arguments"""
    yield ck.cookiecutter(".", output_dir=tmp_path, no_input=True)


def tests_template_renders_ok(template):
    """Checks we can invoke cookiecutter simply without specific arguments"""
    pass  # Checking the "template" fixture doesn't fail the test


@pytest.fixture
def template_deps(template):
    """Install dependencies inside template via poetry install"""
    subprocess.check_call(["poetry", "install"], cwd=template)
    yield template


def tests_template_deps_ok(template_deps):
    """Checks we can install dev dependencies via poetry install"""
    pass


def tests_template_packages_ok(template_deps):
    """Checks we can run poetry build on rendered code to get a binary"""
    subprocess.check_call(["poetry", "build"], cwd=template_deps)
    assert os.listdir(template_deps + "/dist/"), "Nothing was built!"


def tests_template_makes_ok(template):
    """Checks we can run make on rendered code to get a binary/tests"""
    subprocess.check_call(["make"], cwd=template)
    assert os.listdir(template + "/dist/"), "Nothing was built!"
    assert os.path.isfile(
        template + "/test_results/results.xml"
    ), "Test results not saved"
    assert os.path.isfile(
        template + "/test_results/coverage.xml"
    ), "Coverage report not saved"
    assert os.path.isfile(
        template + "/test_results/flake8.txt"
    ), "Linter results not saved"
    git_changes_post_make = subprocess.run(
        ["git", "diff-files", "--quiet"], cwd=template
    )
    assert (
        git_changes_post_make.returncode == 0
    ), "Git found unstaged files after running 'make'"


def tests_cli_runs_usage(template_deps):
    """Runs the generated CLI to get usage info"""
    cmd = subprocess.run(
        ["poetry", "run", DEFAULT_CONF["project_slug"]],
        cwd=template_deps,
        capture_output=True,
        text=True,
    )
    assert cmd.returncode > 0, "Missing param should show as nonzero exit code"
    assert "usage" in cmd.stderr, "Running CLI entrypoint should show usage"


def tests_template_is_git_repo(template):
    """Checks rendered code is a git repo"""
    # git status fails on a non-repo
    subprocess.check_call(["git", "status"], cwd=template)


class CasesDockerBuild:
    """Test cases for the docker-building commands"""

    def case_docker_build_dev(self):
        """Build the dev container via make"""
        return (["make", "docker-build"], DEFAULT_CONF["project_slug"] + "-dev")

    def case_docker_build_release(self):
        """Build the release container via make"""
        return (["make", "docker-build-release"], DEFAULT_CONF["project_slug"])


@parametrize_with_cases("make_cmd,img_name", cases=CasesDockerBuild)
def tests_template_makes_docker_ok(template, make_cmd, img_name):
    """Checks we can build a docker image on rendered code"""
    subprocess.check_call(make_cmd, cwd=template)
    subprocess.check_call(["docker", "image", "rm", img_name])
