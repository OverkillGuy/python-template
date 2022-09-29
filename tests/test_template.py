import os
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import Callable

from cookiecutter.generate import generate_context
from cookiecutter.prompt import prompt_for_config
from pytest_cases import fixture, parametrize, parametrize_with_cases

from tests.docker import run_docker_devimg, run_native
from tests.templating import (
    RANDOMIZED_PROJECT_NAME,
    Template,
    cookiecutter_json,
    expand_template,
)

ROOT_COOKIECUTTER_JSON = cookiecutter_json()


@fixture
@parametrize(runfunc=[run_native, run_docker_devimg])
@parametrize(python_version=ROOT_COOKIECUTTER_JSON["python_version"])
def template(python_version: str, runfunc: Callable):
    """Template expansion fixture, parametrized by python version"""
    extra_context = {
        "python_version": python_version,
        "project_name": RANDOMIZED_PROJECT_NAME,
    }
    conf = prompt_for_config(
        generate_context(extra_context=extra_context), no_input=True
    )
    with TemporaryDirectory() as tmp_path:
        path = expand_template(tmp_path, extra_context)
        yield Template(path, conf, runfunc)


def tests_template_renders_ok(template: Template):
    """Checks we can invoke cookiecutter simply without specific arguments"""
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


# class CasesDockerBuild:
#     """Test cases for the docker-building commands"""

#     def case_docker_build_dev(self, template: Template):
#         """Build the dev container via make"""
#         return (["make", "docker-build-dev"], template.context["project_slug"] + "-dev")

#     def case_docker_build_release(self, template: Template):
#         """Build the release container via make"""
#         return (["make", "docker-build-release"], template.context["project_slug"])


# @parametrize_with_cases("make_cmd,img_name", cases=CasesDockerBuild)
# def tests_template_makes_docker_ok(template, make_cmd, img_name):
#     """Checks we can build a docker image on rendered code"""
#     subprocess.check_call(make_cmd, cwd=template.path)
#     subprocess.check_call(["docker", "image", "rm", img_name])
