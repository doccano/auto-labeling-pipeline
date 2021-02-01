import abc
from typing import Dict, Iterable, List, Optional

from auto_labeling_pipeline.label import Label


class Labels(metaclass=abc.ABCMeta):

    def __init__(self, labels: List[Label]):
        self.labels = labels

    def filter_by_name(self, vocabulary: Optional[Iterable[str]] = None) -> 'Labels':
        if not vocabulary:
            return self
        labels = [label for label in self.labels if label.included(vocabulary)]
        return self.__class__(labels)

    def replace_label(self, mapping: Optional[Dict[str, str]] = None) -> 'Labels':
        if not mapping:
            return self
        self.labels = [label.replace(mapping) for label in self.labels]
        return self.__class__(self.labels)

    def dict(self) -> List[dict]:
        return [label.dict() for label in self.labels]


class ClassificationLabels(Labels):
    pass


class SequenceLabels(Labels):
    pass


class Seq2seqLabels(Labels):

    def filter_by_name(self, vocabulary: Optional[Iterable[str]] = None) -> Labels:
        return self

    def replace_label(self, mapping: Optional[Dict[str, str]] = None) -> Labels:
        return self
