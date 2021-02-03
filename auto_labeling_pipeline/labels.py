import abc
from typing import Dict, Iterable, List, Optional, Type

from auto_labeling_pipeline.label import ClassificationLabel, Label, Seq2seqLabel, SequenceLabel


class Labels(metaclass=abc.ABCMeta):
    label_class: Type[Label]

    def __init__(self, labels: List[Dict]):
        self.labels = [self.label_class(**label) for label in labels]

    def filter_by_name(self, vocabulary: Optional[Iterable[str]] = None) -> 'Labels':
        if not vocabulary:
            return self
        labels = [label.dict() for label in self.labels if label.included(vocabulary)]
        return self.__class__(labels)

    def replace_label(self, mapping: Optional[Dict[str, str]] = None) -> 'Labels':
        if not mapping:
            return self
        labels = [label.replace(mapping).dict() for label in self.labels]
        return self.__class__(labels)

    def dict(self) -> List[dict]:
        return [label.dict() for label in self.labels]


class ClassificationLabels(Labels):
    label_class = ClassificationLabel


class SequenceLabels(Labels):
    label_class = SequenceLabel


class Seq2seqLabels(Labels):
    label_class = Seq2seqLabel

    def filter_by_name(self, vocabulary: Optional[Iterable[str]] = None) -> Labels:
        return self

    def replace_label(self, mapping: Optional[Dict[str, str]] = None) -> Labels:
        return self
