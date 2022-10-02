"""Command line entrypoint for {{ cookiecutter.project_slug }}"""
import argparse
import sys
from typing import List, Optional


def parse_arguments(arguments: List[str]) -> argparse.Namespace:
    """Parse generic arguments, given as parameters"""
    parser = argparse.ArgumentParser(
        "{{ cookiecutter.project_slug }}", description="{{cookiecutter.description}}"
    )
    parser.add_argument("foo", help="Some parameter")
    return parser.parse_args(arguments)


def cli(arguments: Optional[List[str]] = None):
    """Run the {{ cookiecutter.package_name }} cli"""
    if arguments is None:
        arguments = sys.argv[1:]
    args = parse_arguments(arguments)
    print(f"Foo is: {args.foo}")
    # Do the actual thing!
