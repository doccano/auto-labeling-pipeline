from typing import List, Type

from pydantic import BaseModel

from auto_labeling_pipeline.mappings import AmazonComprehendSentimentTemplate, GCPEntitiesTemplate, MappingTemplate
from auto_labeling_pipeline.models import (AmazonComprehendSentimentRequestModel, CustomRESTRequestModel,
                                           GCPEntitiesRequestModel, RequestModel)
from auto_labeling_pipeline.postprocessing import BasePostProcessor, PostProcessor
from auto_labeling_pipeline.task import Task


class Option(BaseModel):
    name: str
    task: Task
    model: Type[RequestModel]
    template: Type[MappingTemplate]
    post_processor: Type[BasePostProcessor] = PostProcessor

    class Config:
        arbitrary_types_allowed = True


class Options:
    options = [
        Option(
            name='Custom REST Request',
            task=Task('Any'),
            model=CustomRESTRequestModel,
            template=MappingTemplate
        ),
        Option(
            name='Amazon Comprehend Sentiment Analysis',
            task=Task('TextClassification'),
            model=AmazonComprehendSentimentRequestModel,
            template=AmazonComprehendSentimentTemplate
        ),
        Option(
            name='GCP Entity Analysis',
            task=Task('SequenceLabeling'),
            model=GCPEntitiesRequestModel,
            template=GCPEntitiesTemplate
        )
    ]

    @classmethod
    def filter_by_task(cls, task_name: str) -> List[Option]:
        task = Task(task_name)
        return [option for option in cls.options if option.task == task]

    @classmethod
    def find(cls, option_name: str) -> Option:
        for option in cls.options:
            if option.name == option_name:
                return option
        raise ValueError('Option {} is not found.'.format(option_name))
