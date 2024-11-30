"""Useful utilities relating to docker containers"""
import subprocess
import sys
import tarfile
from io import BytesIO

import docker
import pytest

from tests.templating import Template

from testcontainers.core.image import DockerImage
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_container_is_ready


def docker_or_skip():
    """Get the docker client or skip tests that try it"""
    try:
        return docker.from_env()
    except docker.errors.DockerException:
        pytest.skip("No docker-socket connection")


def copy_container_path_out(container, path, destination):
    """Copy a container's path out into destination/"""
    tar_stream, stats = container._container.get_archive(path, encode_stream=True)
    tar_bytestring = BytesIO()
    for chunk in tar_stream:
        tar_bytestring.write(chunk)
    tar_bytestring.seek(0)  # Rewind the in-memory tar file for data-extraction
    with tarfile.open(fileobj=tar_bytestring, mode="r") as tar_file:
        tar_file.extractall(destination)


def python_dev_image(template: Template):
    """Build the python image of the template's dockerfile"""


def run_docker_devimg(
    command: list[str],
    template: Template,
    raise_on_nonzero_exitcode=True,
):
    """Run the given command in the dev image

    Emulate a docker build + docker run + docker cp via docker-py
    """
    workdir, context, _runfunc = template
    py_version = template.context["python_version"]
    copy_source_path = "/workdir"
    docker_devimg_name = f"python-skeleton-testing:{py_version}"
    with DockerImage(
        path=template.path, tag=docker_devimg_name, clean_up=True
    ) as image:
        with DockerContainer(str(image)).with_command(command).with_env(
            "XDG_CACHE_HOME", "/caches/"
        ).with_volume_mapping(
            f"python-skeleton-test-{context['python_version']}", "/caches", "rw"
        )as container:
# .with_volume_mapping(template.path + "/.git/", "/workdir/.git/", "ro")
            wait_container_is_ready()
            exit_code = container.get_wrapped_container().wait()["StatusCode"]
            logs = container.get_logs()
            print(logs)
            copy_container_path_out(container, copy_source_path, workdir)
    if exit_code > 0:
        pytest.fail(f"Build unsuccessful, container exited {exit_code}")
    # Successful run: copy data back out for analysis
    return workdir + copy_source_path


def run_native(command: list[str], template: Template):
    """Run the given command in Template env natively (no-docker)"""
    # Ensure the deps are installed already
    try:
        subprocess.run(
            ["poetry", "install"],
            cwd=template.path,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        # breakpoint()
        if "ython version" in e.stderr.lower():
            pytest.skip(
                "Missing python executable for version "
                f"{template.context['python_version']}"
            )
        elif "is not allowed by the project" in e.stderr.lower():
            pytest.skip("Python version too low for project")
        else:
            print(e.stdout)
            print(e.stderr, file=sys.stderr)
            raise e
    try:
        subprocess.run(
            command,
            cwd=template.path,
            capture_output=True,
            text=True,
            check=True,
        )
        return template.path
    except subprocess.CalledProcessError as e:
        # Explicitly print the failing logs before leaving
        print(e.stdout)
        print(e.stderr, file=sys.stderr)
        raise e
