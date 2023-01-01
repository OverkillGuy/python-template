"""Useful utilities relating to docker containers"""
import subprocess
import sys
import tarfile
from io import BytesIO

import docker
import pytest

from tests.templating import Template


def docker_or_skip():
    """Get the docker client or skip tests that try it"""
    try:
        return docker.from_env()
    except docker.errors.DockerException:
        pytest.skip("No docker-socket connection")


def print_docker_build_log(build_log_stream):
    """Convert a docker build log JSON stream to string"""
    log_item = next(build_log_stream)
    log_acc = ""
    # Exhaust the "stream" key while we aren't erroring
    while "error" not in log_item:
        log_acc += log_item["stream"]
        # TODO: Print separate newline on multiple \n in log_acc
        if "\n" in log_acc:
            print(log_acc)
            log_acc = ""
        log_item = next(build_log_stream)
    # Reached the error: print it and quit
    print(log_item["error"], file=sys.stderr)
    print(log_item["errorDetail"], file=sys.stderr)


def copy_container_path_out(container, path, destination):
    """Copy a container's path out into destination/"""
    tar_stream, stats = container.get_archive(path, encode_stream=True)
    tar_bytestring = BytesIO()
    for chunk in tar_stream:
        tar_bytestring.write(chunk)
    tar_bytestring.seek(0)  # Rewind the in-memory tar file for data-extraction
    with tarfile.open(fileobj=tar_bytestring, mode="r") as tar_file:
        tar_file.extractall(destination)


def python_dev_image(template: Template):
    """Build the python image of the template's dockerfile"""
    py_version = template.context["python_version"]
    docker_devimg_name = f"python-skeleton-testing:{py_version}"
    docker_client = docker_or_skip()
    try:
        docker_client.images.build(
            path=str(template.path),
            tag=docker_devimg_name,  # FIXME: Clashing parallel builds
            rm=True,
        )
    except (docker.errors.BuildError) as e:
        print("Failed to build the main templated Dockerfile. Build log:")
        print_docker_build_log(e.build_log)
        raise e
    return docker_devimg_name


def run_docker_devimg(
    command,
    template: Template,
    raise_on_nonzero_exitcode=True,
):
    """Run the given command in the dev image

    Emulate a docker build + docker run + docker cp via docker-py
    """
    workdir, context, _runfunc = template
    docker_devimg_name = python_dev_image(template)
    docker_client = docker_or_skip()
    try:
        container = docker_client.containers.run(
            image=docker_devimg_name,
            command=command,
            volumes=[
                # Named volume mount for ownership
                f"python-skeleton-test-{context['python_version']}:/caches:rw",
            ],
            stdout=True,
            stderr=True,
            environment={"XDG_CACHE_HOME": "/caches/"},
            detach=True,
        )
        # Block till container completed
        # TODO: Confirm timeout unit (sec?)
        response = container.wait(timeout=90)
        exit_code = response["StatusCode"]
        print(container.logs())
        if exit_code > 0:
            pytest.fail(f"Build unsuccessful, container exited {exit_code}")
        # Successful run: copy data back out for analysis
        copy_source_path = "/workdir"
        copy_container_path_out(container, copy_source_path, workdir)
        return workdir + copy_source_path
    except (
        docker.errors.ContainerError,
        docker.errors.APIError,
    ) as e:
        # Explicitly get container's logs, since it may be empty
        if raise_on_nonzero_exitcode:
            logs = docker_client.containers.get(e.container.name).logs()
            pytest.fail(
                f"Failed running {command} error was: {e}. Container logs: {logs}"
            )


def run_native(command, template: Template):
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
