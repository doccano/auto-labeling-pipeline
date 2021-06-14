from typing import List, Type

from pydantic import BaseModel

from auto_labeling_pipeline import mappings as mp
from auto_labeling_pipeline import models as mo
from auto_labeling_pipeline import task as t


class Option(BaseModel):
    name: str
    description: str
    task: Type[t.Task]
    model: Type[mo.RequestModel]
    template: Type[mp.MappingTemplate]

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
        task = t.TaskFactory.create(task_name)
        return [option for option in cls.options if option.task == task or option.task == t.GenericTask]

    @classmethod
    def find(cls, option_name: str) -> Option:
        for option in cls.options:
            if option.name == option_name:
                return option
        raise ValueError('Option {} is not found.'.format(option_name))

    @classmethod
    def register(cls, task: Type[t.Task], model: Type[mo.RequestModel], template: Type[mp.MappingTemplate]):
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


Options.register(
    t.GenericTask,
    mo.CustomRESTRequestModel,
    mp.MappingTemplate
)
Options.register(
    t.DocumentClassification,
    mo.AmazonComprehendSentimentRequestModel,
    mp.AmazonComprehendSentimentTemplate
)
Options.register(
    t.SequenceLabeling,
    mo.GCPEntitiesRequestModel,
    mp.GCPEntitiesTemplate
)
Options.register(
    t.SequenceLabeling,
    mo.AmazonComprehendEntityRequestModel,
    mp.AmazonComprehendEntityTemplate
)
Options.register(
    t.SequenceLabeling,
    mo.AmazonComprehendPIIEntityRequestModel,
    mp.AmazonComprehendEntityTemplate
)
Options.register(
    t.ImageClassification,
    mo.GCPImageLabelDetectionRequestModel,
    mp.GCPImageLabelDetectionTemplate
)
Options.register(
    t.ImageClassification,
    mo.AmazonRekognitionLabelDetectionRequestModel,
    mp.AmazonRekognitionLabelDetectionTemplate
)
