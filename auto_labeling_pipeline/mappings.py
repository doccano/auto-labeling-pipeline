import json
import pathlib
from typing import Any, Dict, Optional, Type

from jinja2 import Template

from auto_labeling_pipeline.labels import Labels
from auto_labeling_pipeline.task import DocumentClassification, GenericTask, SequenceLabeling, Task

TEMPLATE_DIR = pathlib.Path(__file__).parent / 'templates'


class MappingTemplate:
    task: Type[Task] = GenericTask
    template_file: str = ''

    def __init__(self, task: Type[Task] = GenericTask, template: Optional[str] = ''):
        if self.template_file:
            template = self.load()
        self.task = self.task or task
        self.template = template

    def render(self, response: Dict) -> Labels:
        template = Template(self.template)
        rendered_json = template.render(input=response)
        labels = json.loads(rendered_json)
        labels = self.task.create_label_collection(labels)
        return labels

    def load(self) -> str:
        filepath = TEMPLATE_DIR / self.template_file
        with open(filepath) as f:
            return f.read()

    def dict(self) -> Dict[str, Any]:
        return {
            'template': self.template,
            'task': self.task
        }


class AmazonComprehendSentimentTemplate(MappingTemplate):
    task = DocumentClassification
    template_file = 'amazon_comprehend_sentiment.jinja2'


class GCPEntitiesTemplate(MappingTemplate):
    task = SequenceLabeling
    template_file = 'gcp_entities.jinja2'
