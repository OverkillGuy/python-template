{{cookiecutter.project_name}}
{% for _ in range(cookiecutter.project_name|length) %}={% endfor %}

Below is the rendered version of the project's :code:`README.md` file, found at the
root of the code repository.

.. include:: ../../README.md
   :parser: myst_parser.sphinx_


.. toctree::
   :caption: Table of Contents:

   Changelog <changelog>
   architecture
   API Reference <autoapi/{{ cookiecutter.package_name }}/index>
