"""Cookiecutter templating-related utilities"""

from collections import namedtuple
from pathlib import Path

import faker_microservice
import yaml
from copier import run_copy as copier
from faker import Faker

Template = namedtuple("Template", ["path", "context", "run_in_dev"])

fake = Faker()
fake.add_provider(faker_microservice.Provider)

# Use the Faker lib to generate a plausible project name
RANDOMIZED_PROJECT_NAME = (
    fake.microservice().replace("-", " ").replace("_", " ").capitalize()
)


def expand_template(tmp_path, extra_context=None):
    """Expand a single template"""
    copier(src_path=".", dst_path=tmp_path, data=extra_context, defaults=True)
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
