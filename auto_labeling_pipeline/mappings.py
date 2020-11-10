import json
import pathlib
from typing import Optional, Type, Union

from jinja2 import Template

from auto_labeling_pipeline.label import ClassificationLabel, Seq2seqLabel, SequenceLabel

TEMPLATE_DIR = pathlib.Path(__file__).parent / 'templates'
LABEL_CLASS = Type[Union[ClassificationLabel, Seq2seqLabel, SequenceLabel]]


class MappingTemplate:
    label_class: LABEL_CLASS = ClassificationLabel
    template_file: str = ''

    def __init__(self, template: Optional[str] = None):
        if self.template_file:
            template = self.load()
        self.template = Template(template)

    def render(self, response: dict):
        rendered_json = self.template.render(input=response)
        labels = json.loads(rendered_json)
        labels = [self.label_class(**label) for label in labels]
        return labels

    def load(self) -> str:
        filepath = TEMPLATE_DIR / self.template_file
        with open(filepath) as f:
            return f.read()


class AmazonComprehendSentimentTemplate(MappingTemplate):
    label_class = ClassificationLabel
    template_file = 'amazon_comprehend_sentiment.jinja2'


class GCPEntitiesTemplate(MappingTemplate):
    label_class = SequenceLabel
    template_file = 'gcp_entities.jinja2'
