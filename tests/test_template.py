import os
import subprocess
from tempfile import TemporaryDirectory
from typing import Callable

import pytest
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
@parametrize(dynamic_versioning=[True, False])
@parametrize(python_version=ROOT_CONFIG["python_version"]["choices"])
def template(python_version: str, dynamic_versioning: bool, runfunc: Callable):
    """Template expansion fixture, parametrized by python version etc"""
    extra_context = {
        "python_version": python_version,
        "project_name": RANDOMIZED_PROJECT_NAME,
        "description": "A cool project",
        "dynamic_versioning": dynamic_versioning,
    }
    with TemporaryDirectory() as tmp_path:
        path, config = expand_template(tmp_path, extra_context)
        # git_init(path, config["author_name"], config["author_email"])
        yield Template(path, config, runfunc)


# TODO Separate the parametrization of runfunc to avoid testing twice basic features
def tests_template_renders_ok(template: Template):
    """Checks we can invoke copier simply without specific arguments"""
    pass  # Checking the "template" fixture doesn't fail the test

def tests_template_makes_ok(template: Template):
    """Scenario: Running 'make' on template applies full build process"""
    # Given a template
    # When I run 'make'
    out_path = template.run_in_dev(["make"], template)
    # Then the command succeeds
    # And I get test results
    assert os.path.isfile(
        out_path + "/test_results/results.xml"
    ), "Should save test results jUnit results"
    # And I get test coverage
    assert os.path.isfile(
        out_path + "/test_results/coverage.xml"
    ), "Should save coverage"
    # And I get generated docs in HTML
    assert os.listdir(out_path + "/docs/build/html/"), "Should build docs"
    # And I get built packages
    assert os.listdir(out_path + "/dist/"), "Should build package"
    # And 'git status' doesn't show any file to edit
    git_changes_post_make = subprocess.run(
        ["git", "status", "--short"],
        cwd=out_path,
        capture_output=True,
        text=True,
    )
    assert (
        not git_changes_post_make.stdout
    ), "Should have no unstaged files after running 'make'"


def tests_cli_runs_ok(template: Template):
    """Runs the generated CLI's help works"""
    template.run_in_dev(["uv", "run", template.context['project_slug'],"--help"], template)


def tests_template_makes_docker_release_ok(template: Template):
    """Checks we can build the released docker image"""
    subprocess.check_call(["make", "docker-build-release"], cwd=template.path)
    image_name = template.context["project_slug"] + ":0.1.0"
    subprocess.check_call(["docker", "image", "rm", image_name])

def tests_template_makes_docker_dev_ok(template: Template):
    """Checks we can build the dev docker image"""
    subprocess.check_call(["make", "docker-build-dev"], cwd=template.path)
    image_name = template.context["project_slug"] + "-dev"
    subprocess.check_call(["docker", "image", "rm", image_name])



@parametrize(
    bad_project_name=[
        "",
        "lower-kebab-case",
    ]
)
def tests_bad_projectname(bad_project_name):
    """Scenario: Bad project name gets rejected"""
    # Given a bad project name
    extra_context = {
        "project_name": bad_project_name,
        "description": "A cool project",
    }
    # When I render the template
    # Then I get a validation error
    with pytest.raises(ValueError):
        with TemporaryDirectory() as tmp_path:
            _path, _config = expand_template(tmp_path, extra_context)
