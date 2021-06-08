import abc
from typing import Type

from auto_labeling_pipeline.labels import ClassificationLabels, Labels, Seq2seqLabels, SequenceLabels


class Task(abc.ABC):
    label_collection: Type[Labels]


class GenericTask(Task):
    label_collection = Labels


class DocumentClassification(Task):
    label_collection = ClassificationLabels


class SequenceLabeling(Task):
    label_collection = SequenceLabels


class Seq2seq(Task):
    label_collection = Seq2seqLabels


class ImageClassification(Task):
    label_collection = ClassificationLabels


class TaskFactory:

    @classmethod
    def create(cls, task_name: str) -> Type[Task]:
        return {
            'DocumentClassification': DocumentClassification,
            'SequenceLabeling': SequenceLabeling,
            'Seq2seq': Seq2seq,
            'ImageClassification': ImageClassification
        }.get(task_name, GenericTask)
