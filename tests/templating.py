"""Cookiecutter templating-related utilities"""

from collections import namedtuple

from cookiecutter import main as ck

Template = namedtuple("Template", ["path", "context"])


def expand_template(tmp_path, extra_context=None):
    """Expand a single template"""
    return ck.cookiecutter(
        ".", extra_context=extra_context, output_dir=tmp_path, no_input=True
    )
