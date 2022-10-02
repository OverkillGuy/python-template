"""Command line entrypoint for {{ cookiecutter.project_slug }}"""
import argparse
{% if cookiecutter.project_variant == "REST_API_client" %}
import os
{% endif %}
import sys
from typing import Optional

{% if cookiecutter.project_variant == "REST_API_client" %}
from {{ cookiecutter.package_name }}.api import Secret, get_from_api
{# Empty line here to make the import have 2 lines below it for PEP8 #}

{% endif %}

def parse_arguments(arguments: list[str]) -> argparse.Namespace:
    """Parse generic arguments, given as parameters"""
    parser = argparse.ArgumentParser(
        "{{ cookiecutter.project_slug }}",
        description="{{cookiecutter.description}}",
{% if cookiecutter.project_variant == "REST_API_client" %}
        epilog="API token requires either --token-file flag or envvar API_TOKEN",
{% endif %}
    )
{% if cookiecutter.project_variant == "REST_API_client" %}
    parser.add_argument(
        "--token-file", help="File containing API Token", type=argparse.FileType("r")
    )
{% else %}
    parser.add_argument("foo", help="Some parameter")
{% endif %}
    return parser.parse_args(arguments)


def cli(arguments: Optional[list[str]] = None):
    """Run the {{ cookiecutter.package_name }} cli"""
    if arguments is None:
        arguments = sys.argv[1:]
    args = parse_arguments(arguments)
{% if cookiecutter.project_variant == "REST_API_client" %}
    if args.token_file:
        token = args.token_file.read().strip()
    else:
        token = os.getenv("API_TOKEN")
    if token is None:
        print(
            "Missing API token: --token-file or set API_TOKEN envvar", file=sys.stderr
        )
        exit(2)  # Simulate the argparse behaviour of exiting on bad args
    main(token)


def main(token: Secret):
    """Run the program's main command"""
    api_response: dict = get_from_api(token)
    print(api_response)
{% else %}
    main(args.foo)


def main(foo):
    """Run the program's main command"""
    print(f"Foo is: {foo}")
{% endif %}
