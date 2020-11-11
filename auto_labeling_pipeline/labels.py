import abc
from typing import Optional, Sequence, Set

from pydantic import BaseModel

from auto_labeling_pipeline.label import ClassificationLabel, Seq2seqLabel, SequenceLabel


class Labels(metaclass=abc.ABCMeta):

    def __init__(self, labels: Sequence[BaseModel]):
        self.labels = labels

    @abc.abstractmethod
    def filter_by_name(self, stop_labels: Optional[Set[str]] = None) -> 'Labels':
        raise NotImplementedError

    @abc.abstractmethod
    def convert_label(self, mapping: Optional[dict] = None) -> 'Labels':
        raise NotImplementedError

    def dict(self) -> Sequence[dict]:
        return [label.dict() for label in self.labels]


class ClassificationLabels(Labels):

    def __init__(self, labels: Sequence[ClassificationLabel]):
        super().__init__(labels)
        self.labels: Sequence[ClassificationLabel] = labels

    def filter_by_name(self, stop_labels: Optional[Set[str]] = None) -> 'ClassificationLabels':
        if not stop_labels:
            return self
        labels = [a for a in self.labels if a.label not in stop_labels]
        return ClassificationLabels(labels)

    def convert_label(self, mapping: Optional[dict] = None) -> 'ClassificationLabels':
        if not mapping:
            return self
        for a in self.labels:
            label = a.label
            if label in mapping:
                a.label = mapping[label]
        return ClassificationLabels(self.labels)


class SequenceLabels(Labels):

    def __init__(self, labels: Sequence[SequenceLabel]):
        super().__init__(labels)
        self.labels: Sequence[SequenceLabel] = labels

    def filter_by_name(self, stop_labels: Optional[Set[str]] = None) -> 'SequenceLabels':
        if not stop_labels:
            return self
        labels = [a for a in self.labels if a.label not in stop_labels]
        return SequenceLabels(labels)

    def convert_label(self, mapping: Optional[dict] = None) -> 'SequenceLabels':
        if not mapping:
            return self
        for a in self.labels:
            label = a.label
            if label in mapping:
                a.label = mapping[label]
        return SequenceLabels(self.labels)


class Seq2seqLabels(Labels):

    def __init__(self, labels: Sequence[Seq2seqLabel]):
        super().__init__(labels)
        self.labels: Sequence[Seq2seqLabel] = labels

    def filter_by_name(self, stop_labels: Optional[Set[str]] = None) -> 'Seq2seqLabels':
        return self

    def convert_label(self, mapping: Optional[dict] = None) -> 'Seq2seqLabels':
        return self
