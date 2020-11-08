import json

from jinja2 import Template


class MappingTemplate:

    def __init__(self, template=None):
        self.template = Template(template)

    def render(self, response: dict):
        rendered_str = self.template.render(input=response)
        rendered_dic = json.loads(rendered_str)
        return rendered_dic


class AmazonComprehendSentimentTemplate(MappingTemplate):

    def __init__(self, template=None):
        template = '[{"label": "{{ input.Sentiment }}"}]'
        super(AmazonComprehendSentimentTemplate, self).__init__(template)
