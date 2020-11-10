import abc
from typing import List, Optional, Set, TypeVar

from auto_labeling_pipeline.label import ClassificationLabel, Seq2seqLabel, SequenceLabel

T = TypeVar('T', ClassificationLabel, Seq2seqLabel, SequenceLabel)


class PostProcessor(metaclass=abc.ABCMeta):

    def __init__(self, stop_labels: Optional[Set] = None, mapping: Optional[dict] = None):
        self.stop_labels = stop_labels
        self.mapping = mapping

    def transform(self, annotations: List[T]) -> List[T]:
        annotations = self.filter_by_label(annotations)
        annotations = self.convert_label(annotations)
        annotations = self.deduplicate(annotations)
        return annotations

    def filter_by_label(self, annotations: List[T]) -> List[T]:
        if not self.stop_labels:
            return annotations
        return [a for a in annotations if a.label not in self.stop_labels]

    def convert_label(self, annotations: List[T]) -> List[T]:
        if not self.mapping:
            return annotations
        for a in annotations:
            label = a.label
            if label in self.mapping:
                a.label = self.mapping[label]
        return annotations

    def deduplicate(self, annotations: List[T]) -> List[T]:
        return annotations


class ClassificationPostProcessor(PostProcessor):
    pass


class SequencePostProcessor(PostProcessor):
    pass


class Seq2seqPostProcessor(PostProcessor):

    def filter_by_label(self, annotations: List[T]) -> List[T]:
        return annotations

    def convert_label(self, annotations: List[T]) -> List[T]:
        return annotations
