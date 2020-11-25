from typing import Any, Type

from auto_labeling_pipeline.label import ClassificationLabel, Label, Seq2seqLabel, SequenceLabel
from auto_labeling_pipeline.labels import ClassificationLabels, Labels, Seq2seqLabels, SequenceLabels


class Task:

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        if self.name == 'Any':
            return True
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    @property
    def label_class(self) -> Type[Label]:
        task_to_label = {
            'TextClassification': ClassificationLabel,
            'SequenceLabeling': SequenceLabel,
            'Seq2seq': Seq2seqLabel
        }
        return task_to_label[self.name]

    @property
    def label_collection(self) -> Type[Labels]:
        task_to_collection = {
            'TextClassification': ClassificationLabels,
            'SequenceLabeling': SequenceLabels,
            'Seq2seq': Seq2seqLabels
        }
        return task_to_collection[self.name]
