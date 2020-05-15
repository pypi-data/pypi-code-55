from django.forms.widgets import MediaDefiningClass
from django.template.base import Context


class Component(metaclass=MediaDefiningClass):
    template: str = ""

    def context(self, *args, **kwargs):
        return kwargs

    def render(self, child_nodes, context: Context, component_context: dict) -> str:
        for key, value in component_context.items():
            context[key] = value
        context["children"] = child_nodes.render(context)
        template = context.template.engine.get_template(self.template)
        return template.render(context)
