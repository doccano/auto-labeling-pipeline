from typing import List, Type

from pydantic import BaseModel

from auto_labeling_pipeline.mappings import AmazonComprehendSentimentTemplate, GCPEntitiesTemplate, MappingTemplate
from auto_labeling_pipeline.models import (AmazonComprehendSentimentRequestModel, CustomRESTRequestModel,
                                           GCPEntitiesRequestModel, RequestModel)
from auto_labeling_pipeline.task import DocumentClassification, GenericTask, SequenceLabeling, Task, TaskFactory


class Option(BaseModel):
    name: str
    description: str
    task: Type[Task]
    model: Type[RequestModel]
    template: Type[MappingTemplate]

    class Config:
        arbitrary_types_allowed = True

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'schema': self.model.schema(),
            'template': self.template().template
        }


class Options:
    options = [
        Option(
            name='Custom REST Request',
            description='This allow you to call some REST API.',
            task=GenericTask,
            model=CustomRESTRequestModel,
            template=MappingTemplate
        ),
        Option(
            name='Amazon Comprehend Sentiment Analysis',
            description='This allow you to determine the sentiment of a text by '
                        '<a href="https://docs.aws.amazon.com/en_us/comprehend/">Amazon Comprehend</a>.',
            task=DocumentClassification,
            model=AmazonComprehendSentimentRequestModel,
            template=AmazonComprehendSentimentTemplate
        ),
        Option(
            name='GCP Entity Analysis',
            description='This allow you to analyze entities in a text by '
                        '<a href="https://cloud.google.com/natural-language/docs/analyzing-entities">'
                        'Cloud Natural Language API</a>.',
            task=SequenceLabeling,
            model=GCPEntitiesRequestModel,
            template=GCPEntitiesTemplate
        )
    ]

    @classmethod
    def filter_by_task(cls, task_name: str) -> List[Option]:
        task = TaskFactory.create(task_name)
        return [option for option in cls.options if option.task == task or option.task == GenericTask]

    @classmethod
    def find(cls, option_name: str) -> Option:
        for option in cls.options:
            if option.name == option_name:
                return option
        raise ValueError('Option {} is not found.'.format(option_name))
