import json
import pathlib
from typing import Optional, Type, Union

from jinja2 import Template

from auto_labeling_pipeline.label import ClassificationLabel, Seq2seqLabel, SequenceLabel
from auto_labeling_pipeline.labels import ClassificationLabels, Labels, Seq2seqLabels, SequenceLabels

TEMPLATE_DIR = pathlib.Path(__file__).parent / 'templates'
LABEL_CLASS = Type[Union[ClassificationLabel, Seq2seqLabel, SequenceLabel]]
LABELS_CLASS = Type[Union[ClassificationLabels, Seq2seqLabels, SequenceLabels]]


class MappingTemplate:
    label_class: LABEL_CLASS = ClassificationLabel
    labels_class: LABELS_CLASS = ClassificationLabels
    template_file: str = ''

    def __init__(self, template: Optional[str] = None):
        if self.template_file:
            template = self.load()
        self.template = Template(template)

    def render(self, response: dict) -> Labels:
        rendered_json = self.template.render(input=response)
        labels = json.loads(rendered_json)
        labels = [self.label_class(**label) for label in labels]
        return self.labels_class(labels)

    def load(self) -> str:
        filepath = TEMPLATE_DIR / self.template_file
        with open(filepath) as f:
            return f.read()


class AmazonComprehendSentimentTemplate(MappingTemplate):
    label_class = ClassificationLabel
    labels_class = ClassificationLabels
    template_file = 'amazon_comprehend_sentiment.jinja2'


class GCPEntitiesTemplate(MappingTemplate):
    label_class = SequenceLabel
    labels_class = ClassificationLabels
    template_file = 'gcp_entities.jinja2'
