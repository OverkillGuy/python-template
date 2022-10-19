{{cookiecutter.project_name}}
{% for _ in range(cookiecutter.project_name|length) %}={% endfor %}

Welcome! Browse the table of content to inspect this short project's
documentation.


.. toctree::
   :caption: Table of Contents:

   Readme <readme>
   Changelog <changelog>
   architecture
   API Reference <autoapi/{{ cookiecutter.package_name }}/index>
