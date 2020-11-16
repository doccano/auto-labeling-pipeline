import json
import pathlib
from typing import Dict, Optional, Type

from jinja2 import Template

from auto_labeling_pipeline.label import ClassificationLabel, Label, Seq2seqLabel, SequenceLabel
from auto_labeling_pipeline.labels import ClassificationLabels, Labels, Seq2seqLabels, SequenceLabels

TEMPLATE_DIR = pathlib.Path(__file__).parent / 'templates'


class MappingTemplate:
    task: str = ''
    template_file: str = ''

    def __init__(self, task: str = '', template: Optional[str] = None):
        if self.template_file:
            template = self.load()
        self.task = self.task or task
        self.template = template

    def render(self, response: Dict) -> Labels:
        template = Template(self.template)
        rendered_json = template.render(input=response)
        labels = json.loads(rendered_json)
        labels = [self.label_class(**label) for label in labels]
        labels = self.label_collection(labels)
        return labels

    def load(self) -> str:
        filepath = TEMPLATE_DIR / self.template_file
        with open(filepath) as f:
            return f.read()

    def dict(self) -> Dict[str, Optional[str]]:
        return {
            'template': self.template,
            'task': self.task
        }

    @property
    def label_class(self) -> Type[Label]:
        task_to_label = {
            'TextClassification': ClassificationLabel,
            'SequenceLabeling': SequenceLabel,
            'Seq2seq': Seq2seqLabel
        }
        return task_to_label[self.task]

    @property
    def label_collection(self) -> Type[Labels]:
        task_to_collection = {
            'TextClassification': ClassificationLabels,
            'SequenceLabeling': SequenceLabels,
            'Seq2seq': Seq2seqLabels
        }
        return task_to_collection[self.task]


class AmazonComprehendSentimentTemplate(MappingTemplate):
    task = 'TextClassification'
    template_file = 'amazon_comprehend_sentiment.jinja2'


class GCPEntitiesTemplate(MappingTemplate):
    task = 'SequenceLabeling'
    template_file = 'gcp_entities.jinja2'
