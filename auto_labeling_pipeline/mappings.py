import json
import pathlib
from typing import Any, Dict, Optional, Type

from jinja2 import Template

from auto_labeling_pipeline.labels import ClassificationLabels, Labels, SequenceLabels

TEMPLATE_DIR = pathlib.Path(__file__).parent / 'templates'


class MappingTemplate:
    label_collection: Type[Labels]
    template_file: str = ''

    def __init__(self, label_collection: Type[Labels] = Labels, template: Optional[str] = ''):
        if self.template_file:
            template = self.load()
        if label_collection is not Labels:
            self.label_collection = label_collection
        self.template = template

    def render(self, response: Dict) -> Labels:
        template = Template(self.template)
        rendered_json = template.render(input=response)
        labels = json.loads(rendered_json)
        labels = self.label_collection(labels)
        return labels

    def load(self) -> str:
        filepath = TEMPLATE_DIR / self.template_file
        with open(filepath) as f:
            return f.read()

    def dict(self) -> Dict[str, Any]:
        return {
            'template': self.template,
            'collection': self.label_collection
        }


class AmazonComprehendSentimentTemplate(MappingTemplate):
    label_collection = ClassificationLabels
    template_file = 'amazon_comprehend_sentiment.jinja2'


class GCPImageLabelDetectionTemplate(MappingTemplate):
    label_collection = ClassificationLabels
    template_file = 'gcp_image_label_detection.jinja2'


class AmazonComprehendEntityTemplate(MappingTemplate):
    label_collection = SequenceLabels
    template_file = 'amazon_comprehend_entity.jinja2'


class GCPEntitiesTemplate(MappingTemplate):
    label_collection = SequenceLabels
    template_file = 'gcp_entities.jinja2'


class AmazonRekognitionLabelDetectionTemplate(MappingTemplate):
    label_collection = ClassificationLabels
    template_file = 'amazon_rekognition_label_detection.jinja2'
