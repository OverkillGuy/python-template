import os
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import Callable, Literal

from pytest_cases import fixture, parametrize

from tests.docker import run_docker_devimg, run_native
from tests.templating import (
    RANDOMIZED_PROJECT_NAME,
    Template,
    copier_config,
    expand_template,
)

ROOT_CONFIG = copier_config()


@fixture
@parametrize(runfunc=[run_native, run_docker_devimg])
@parametrize(python_version=ROOT_CONFIG["python_version"]["choices"])
def template(python_version: str, runfunc: Callable):
    """Template expansion fixture, parametrized by python version"""
    extra_context = {
        "python_version": python_version,
        "project_name": RANDOMIZED_PROJECT_NAME,
        "description": "A cool project",
    }
    with TemporaryDirectory() as tmp_path:
        path, config = expand_template(tmp_path, extra_context)
        yield Template(path, config, runfunc)


# TODO Separate the parametrization of runfunc to avoid testing twice basic features
def tests_template_renders_ok(template: Template):
    """Checks we can invoke copier simply without specific arguments"""
    pass  # Checking the "template" fixture doesn't fail the test


def tests_template_packages_ok(template: Template):
    """Checks we can run poetry build on rendered code to get a binary"""
    out_path = template.run_in_dev(["poetry", "build"], template)
    assert os.listdir(out_path + "/dist/"), "Nothing was built!"


def tests_template_docs_ok(template: Template):
    """Checks we can run make docson rendered code to get HTML"""
    out_path = template.run_in_dev(["make", "docs"], template)
    assert os.listdir(out_path + "/docs/build/html/"), "Docs not built"


def tests_template_makes_ok(template: Template):
    """Checks we can run make on rendered code to get a binary/tests"""
    out_path = template.run_in_dev("make", template)
    assert os.listdir(out_path + "/dist/"), "Nothing was built!"
    assert os.path.isfile(
        out_path + "/test_results/results.xml"
    ), "Test results not saved"
    assert os.path.isfile(
        out_path + "/test_results/coverage.xml"
    ), "Coverage report not saved"
    assert os.path.isfile(
        out_path + "/test_results/flake8.txt"
    ), "Linter results not saved"
    git_changes_post_make = subprocess.run(
        ["git", "status", "--short"],
        cwd=out_path,
        capture_output=True,
        text=True,
    )
    assert (
        not git_changes_post_make.stdout
    ), "Git found unstaged files after running 'make'"


def tests_cli_runs_ok(template: Template):
    """Runs the generated CLI's help works"""
    template.run_in_dev([template.context["project_slug"], "--help"], template)


def tests_template_makes_docker_release_ok(template: Template):
    """Checks we can build the released docker image"""
    # Build the wheel file first, for releasing
    subprocess.check_call(["make", "docker-build-release"], cwd=template.path)
    image_name = template.context["project_slug"] + ":0.1.0"
    subprocess.check_call(["docker", "image", "rm", image_name])
