import abc
from typing import List, Optional, Set

from auto_labeling_pipeline.label import Label


class Labels(metaclass=abc.ABCMeta):

    def __init__(self, labels: List[Label]):
        self.labels = labels

    def filter_by_name(self, stop_labels: Optional[Set[str]] = None) -> 'Labels':
        if not stop_labels:
            return self
        labels = [label for label in self.labels if not label.included(stop_labels)]
        return self.__class__(labels)

    def replace_label(self, mapping: Optional[dict] = None) -> 'Labels':
        if not mapping:
            return self
        for label in self.labels:
            label.replace(mapping)
        return self.__class__(self.labels)

    def dict(self) -> List[dict]:
        return [label.dict() for label in self.labels]


class ClassificationLabels(Labels):
    pass


class SequenceLabels(Labels):
    pass


class Seq2seqLabels(Labels):

    def filter_by_name(self, stop_labels: Optional[Set[str]] = None) -> Labels:
        return self

    def replace_label(self, mapping: Optional[dict] = None) -> Labels:
        return self
