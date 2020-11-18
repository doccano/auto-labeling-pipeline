from typing import List, Literal, Type

from pydantic import BaseModel

from auto_labeling_pipeline.mappings import AmazonComprehendSentimentTemplate, GCPEntitiesTemplate, MappingTemplate
from auto_labeling_pipeline.models import (AmazonComprehendSentimentRequestModel, CustomRESTRequestModel,
                                           GCPEntitiesRequestModel, RequestModel)
from auto_labeling_pipeline.postprocessing import BasePostProcessor, PostProcessor


class Option(BaseModel):
    name: str
    task: Literal['Any', 'TextClassification', 'SequenceLabeling', 'Seq2seq']
    model: Type[RequestModel]
    template: Type[MappingTemplate]
    post_processor: Type[BasePostProcessor] = PostProcessor


class Options:
    options = [
        Option(
            name='Custom REST Request',
            task='Any',
            model=CustomRESTRequestModel,
            template=MappingTemplate
        ),
        Option(
            name='Amazon Comprehend Sentiment Analysis',
            task='TextClassification',
            model=AmazonComprehendSentimentRequestModel,
            template=AmazonComprehendSentimentTemplate
        ),
        Option(
            name='GCP Entity Analysis',
            task='SequenceLabeling',
            model=GCPEntitiesRequestModel,
            template=GCPEntitiesTemplate
        )
    ]

    @classmethod
    def filter_by_task(cls, task: str) -> List[Option]:
        return list(filter(lambda o: o.task in {task, 'Any'}, cls.options))

    @classmethod
    def find(cls, option_name: str) -> Option:
        for option in cls.options:
            if option.name == option_name:
                return option
        raise ValueError('Option {} is not found.'.format(option_name))
