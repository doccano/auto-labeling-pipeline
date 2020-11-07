from jinja2 import Template


class MappingTemplate:

    def __init__(self, template=None):
        self.template = Template(template)

    def render(self, response: dict):
        rendered = self.template.render(input=response)
        return rendered
