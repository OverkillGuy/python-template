"""Cookiecutter templating-related utilities"""
import json
from collections import namedtuple

import faker_microservice
from cookiecutter import main as ck
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
    return ck.cookiecutter(
        ".", extra_context=extra_context, output_dir=tmp_path, no_input=True
    )


def cookiecutter_json():
    """Return the dict of the root cookiecutter.json"""
    with open("cookiecutter.json", "r") as cookie_file:
        return json.load(cookie_file)
