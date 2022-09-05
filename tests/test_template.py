import os
import subprocess

import pytest
from cookiecutter import main as ck
from cookiecutter.generate import generate_context
from cookiecutter.prompt import prompt_for_config

# The config in cookiecutter.json, once expanded
DEFAULT_CONF = prompt_for_config(generate_context(), no_input=True)


@pytest.fixture
def template(tmp_path):
    """Invokes cookiecutter simply without specific arguments"""
    yield ck.cookiecutter(".", output_dir=tmp_path, no_input=True)


def tests_template_renders_ok(template):
    """Checks we can invoke cookiecutter simply without specific arguments"""
    pass  # Checking the "template" fixture doesn't fail the test


def tests_template_builds_ok(template):
    """Checks we can run poetry install+build on rendered code to get a binary"""
    subprocess.check_call(["poetry", "install"], cwd=template)
    subprocess.check_call(["poetry", "build"], cwd=template)
    assert os.listdir(template + "/dist/"), "Nothing was built!"


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


def tests_template_is_git_repo(template):
    """Checks rendered code is a git repo"""
    # git status fails on a non-repo
    subprocess.check_call(["git", "status"], cwd=template)


@pytest.mark.parametrize(
    "make_cmd,img_name",
    [
        ("docker-build", f"{DEFAULT_CONF['project_slug']}-dev"),
        ("docker-build-release", DEFAULT_CONF["project_slug"]),
    ],
)
def tests_template_makes_docker_ok(template, make_cmd, img_name):
    """Checks we can build a docker image on rendered code"""
    subprocess.check_call(["make", make_cmd], cwd=template)
    subprocess.check_call(["docker", "image", "rm", img_name])
