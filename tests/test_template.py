import os
import subprocess

import docker
import pytest
from cookiecutter import main as ck
from cookiecutter.generate import generate_context
from cookiecutter.prompt import prompt_for_config
from pytest_cases import parametrize_with_cases

EXTRA_CONTEXT = {"python_version": "3.10"}


# The config in cookiecutter.json, once expanded
DEFAULT_CONF = prompt_for_config(
    generate_context(extra_context=EXTRA_CONTEXT), no_input=True
)

DOCKER_CLIENT = docker.from_env()

DOCKER_DEVIMG_NAME = "python-skeleton-testing"


def python_dev_image(template_path):
    """Build the python image of the template's dockerfile"""
    try:
        img = DOCKER_CLIENT.images.build(
            path=str(template_path), tag=DOCKER_DEVIMG_NAME, rm=True
        )
    except (docker.errors.BuildError, docker.errors.APIError) as e:
        pytest.fail(f"Failed to build the main templated Dockerfile: {e}")
    return DOCKER_DEVIMG_NAME


def expand_template(tmp_path):
    """Expand a single template"""
    return ck.cookiecutter(
        ".", extra_context=EXTRA_CONTEXT, output_dir=tmp_path, no_input=True
    )


# TODO: Use pytest-cases to parametrize out the python_version etc
@pytest.fixture
def template(tmp_path):
    """Invokes cookiecutter simply without specific arguments"""
    template_path = expand_template(tmp_path)
    python_dev_image(template_path)
    yield template_path


def docker_run_devimg(command, workdir, raise_on_nonzero_exitcode=True):
    """Run the given command in the dev image"""
    try:
        return DOCKER_CLIENT.containers.run(
            image=DOCKER_DEVIMG_NAME,
            command=command,
            volumes=[f"{workdir}:/app"],
            working_dir="/app",
            stdout=True,
            stderr=True,
            # auto_remove=True,
        )

    except (
        docker.errors.ContainerError,
        docker.errors.APIError,
    ) as e:
        # Explicitly get container's logs, since it may be empty
        if raise_on_nonzero_exitcode:
            logs = DOCKER_CLIENT.containers.get(e.container.name).logs()
            pytest.fail(
                f"Failed running {command} error was: {e}. Container logs: {logs}"
            )


def tests_template_renders_ok(tmp_path):
    """Checks we can invoke cookiecutter simply without specific arguments"""
    expand_template(tmp_path)
    pass  # Checking the "template" fixture doesn't fail the test


def tests_template_packages_ok(template):
    """Checks we can run poetry build on rendered code to get a binary"""
    docker_run_devimg(["poetry", "build"], template)
    assert os.listdir(template + "/dist/"), "Nothing was built!"


def tests_template_docs_ok(template):
    """Checks we can run make docson rendered code to get HTML"""
    docker_run_devimg(["make", "docs"], template)
    assert os.listdir(template + "/docs/build/html/"), "Docs not built"


def tests_template_makes_ok(template):
    """Checks we can run make on rendered code to get a binary/tests"""
    docker_run_devimg(["make"], template)
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


def tests_cli_runs_usage(template):
    """Runs the generated CLI to get usage info"""
    logs = docker_run_devimg([DEFAULT_CONF["project_slug"], "--help"], template)
    assert "usage" in str(logs), "Running CLI entrypoint should show usage"


class CasesDockerBuild:
    """Test cases for the docker-building commands"""

    def case_docker_build_dev(self):
        """Build the dev container via make"""
        return (["make", "docker-build-dev"], DEFAULT_CONF["project_slug"] + "-dev")

    def case_docker_build_release(self):
        """Build the release container via make"""
        return (["make", "docker-build-release"], DEFAULT_CONF["project_slug"])


@parametrize_with_cases("make_cmd,img_name", cases=CasesDockerBuild)
def tests_template_makes_docker_ok(template, make_cmd, img_name):
    """Checks we can build a docker image on rendered code"""
    subprocess.check_call(make_cmd, cwd=template)
    subprocess.check_call(["docker", "image", "rm", img_name])
