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


class GCPEntitiesTemplate(MappingTemplate):

    def __init__(self, template=None):
        template = '''
        [
        {% for entity in input.entities %}
        {% for mention in entity.mentions %}
        {% if mention.text.content == entity.name %}
        {%- set start_offset = mention.text.beginOffset -%}
        {%- set end_offset = start_offset + mention.text.content|length -%}
        {
        "label": "{{ entity.type }}",
        "start_offset": {{ start_offset }},
        "end_offset": {{ end_offset }}
        }
        {% endif %}
        {% endfor %}
        {% if not loop.last %},{% endif %}
        {% endfor %}
        ]
        '''
        super(GCPEntitiesTemplate, self).__init__(template)
