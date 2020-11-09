import json
import pathlib

from jinja2 import Template

from auto_labeling_pipeline.label import ClassificationLabel, SequenceLabel
TEMPLATE_DIR = pathlib.Path(__file__).parent / 'templates'


class MappingTemplate:
    label_class = None
    template_file = None

    def __init__(self, template=None):
        if self.template_file:
            template = self.load()
        self.template = Template(template)

    def render(self, response: dict):
        rendered_str = self.template.render(input=response)
        labels = json.loads(rendered_str)
        labels = [self.label_class(**label) for label in labels]
        return labels

    def load(self):
        filepath = TEMPLATE_DIR / self.template_file
        with open(filepath) as f:
            return f.read()


class AmazonComprehendSentimentTemplate(MappingTemplate):
    label_class = ClassificationLabel
    template_file = 'amazon_comprehend_sentiment.jinja2'


class GCPEntitiesTemplate(MappingTemplate):
    label_class = SequenceLabel
    template_file = 'gcp_entities.jinja2'
