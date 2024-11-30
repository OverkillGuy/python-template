"""Cookiecutter templating-related utilities"""

import subprocess
from collections import namedtuple
from pathlib import Path

import faker_microservice
import yaml
from copier import run_copy as copier
from faker import Faker

Template = namedtuple("Template", ["path", "context", "run_in_dev"])

fake = Faker()
fake.add_provider(faker_microservice.Provider)
Faker.seed(1)  # Fixed seed to get consistent tests

# Use the Faker lib to generate a plausible project name
RANDOMIZED_PROJECT_NAME = (
    fake.microservice().replace("-", " ").replace("_", " ").capitalize()
)


def expand_template(tmp_path, extra_context=None):
    """Expand a single template"""
    copier(
        src_path=".",
        dst_path=tmp_path,
        data=extra_context,
        defaults=True,
        vcs_ref="HEAD",
        unsafe=True,
    )
    return tmp_path, copier_answers(tmp_path)


def copier_config():
    with open("copier.yml", "r") as config_file:
        return yaml.safe_load(config_file)


def copier_answers(template_path):
    if isinstance(template_path, str):
        path = Path(template_path)
    elif isinstance(template_path, Path):
        path = template_path
    with open(path / ".copier-answers.yml", "r") as answers_file:
        return yaml.safe_load(answers_file)


def git_init(path: Path, author_name: str, author_email: str):
    """Create a git repo with initial commit at path"""
    subprocess.check_call(["git", "init"], cwd=path)
    subprocess.check_call(["git", "add", "--all"], cwd=path)
    subprocess.check_call(
        ["git", "config", "--local", "user.name", author_name], cwd=path
    )
    subprocess.check_call(
        ["git", "config", "--local", "user.email", author_email], cwd=path
    )
    subprocess.check_call(
        ["git", "commit", "--message", "Initial commit from 'copier' template"],
        cwd=path,
    )
    subprocess.check_call(
        [
            "git",
            "tag",
            "v0.1.0",
            "--message",
            "First releasable artefact, from template",
        ],
        cwd=path,
    )
    subprocess.check_call(["git", "config", "--unset", "user.name"], cwd=path)
    subprocess.check_call(["git", "config", "--unset", "user.email"], cwd=path)
