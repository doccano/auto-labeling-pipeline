import json

from jinja2 import Template

from auto_labeling_pipeline.label import ClassificationLabel, SequenceLabel


class MappingTemplate:
    label_class = None

    def __init__(self, template=None):
        self.template = Template(template)

    def render(self, response: dict):
        rendered_str = self.template.render(input=response)
        labels = json.loads(rendered_str)
        labels = [self.label_class(**label) for label in labels]
        return labels


class AmazonComprehendSentimentTemplate(MappingTemplate):
    label_class = ClassificationLabel

    def __init__(self, template=None):
        template = '[{"label": "{{ input.Sentiment }}"}]'
        super(AmazonComprehendSentimentTemplate, self).__init__(template)


class GCPEntitiesTemplate(MappingTemplate):
    label_class = SequenceLabel

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
