import abc
from typing import Dict, List, Type

from auto_labeling_pipeline.label import ClassificationLabel, Label, Seq2seqLabel, SequenceLabel
from auto_labeling_pipeline.labels import ClassificationLabels, Labels, Seq2seqLabels, SequenceLabels


class Task(abc.ABC):
    label_class: Type[Label]
    label_collection: Type[Labels]

    @classmethod
    def create_label_collection(cls, labels: List[Dict]) -> Labels:
        _labels = [cls.label_class(**label) for label in labels]
        return cls.label_collection(_labels)


class GenericTask(Task):
    label_class = Label
    label_collection = Labels


class DocumentClassification(Task):
    label_class = ClassificationLabel
    label_collection = ClassificationLabels


class SequenceLabeling(Task):
    label_class = SequenceLabel
    label_collection = SequenceLabels


class Seq2seq(Task):
    label_class = Seq2seqLabel
    label_collection = Seq2seqLabels


class TaskFactory:

    @classmethod
    def create(cls, task_name: str) -> Type[Task]:
        return {
            'DocumentClassification': DocumentClassification,
            'SequenceLabeling': SequenceLabeling,
            'Seq2seq': Seq2seq
        }.get(task_name, GenericTask)
