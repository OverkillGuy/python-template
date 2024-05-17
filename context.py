"""Extend the Jinja template context with more variables, derived from code"""
from copier_templates_extensions import ContextHook


class ContextUpdater(ContextHook):
    def hook(self, context):
        new_vars = {"package_name": context["project_slug"].lower().replace('-', '_')}
        # Returning new_vars alone is NOT enough to SAVE the new context in answers file
        # Add explicitly these new variables in the answers, which will save to file:
        context["_copier_answers"].update(**new_vars)
        return new_vars
