from typing import List, Type

from pydantic import BaseModel

from auto_labeling_pipeline.mappings import (AmazonComprehendEntityTemplate, AmazonComprehendSentimentTemplate,
                                             GCPEntitiesTemplate, MappingTemplate)
from auto_labeling_pipeline.models import (AmazonComprehendEntityRequestModel, AmazonComprehendPIIEntityRequestModel,
                                           AmazonComprehendSentimentRequestModel, CustomRESTRequestModel,
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
    options: List[Option] = []

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

    @classmethod
    def register(cls, task: Type[Task], model: Type[RequestModel], template: Type[MappingTemplate]):
        schema = model.schema()
        cls.options.append(
            Option(
                name=schema.get('title'),
                description=schema.get('description'),
                task=task,
                model=model,
                template=template
            )
        )


Options.register(GenericTask, CustomRESTRequestModel, MappingTemplate)
Options.register(DocumentClassification, AmazonComprehendSentimentRequestModel, AmazonComprehendSentimentTemplate)
Options.register(SequenceLabeling, GCPEntitiesRequestModel, GCPEntitiesTemplate)
Options.register(SequenceLabeling, AmazonComprehendEntityRequestModel, AmazonComprehendEntityTemplate)
Options.register(SequenceLabeling, AmazonComprehendPIIEntityRequestModel, AmazonComprehendEntityTemplate)
