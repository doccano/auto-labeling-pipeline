import abc
from typing import Dict, Iterable

from pydantic import BaseModel


class Label(BaseModel, abc.ABC):

    @abc.abstractmethod
    def included(self, labels: Iterable[str]) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def replace(self, mapping: Dict[str, str]) -> 'Label':
        raise NotImplementedError

    @abc.abstractmethod
    def overlap_with(self, other) -> bool:
        raise NotImplementedError

    def __hash__(self):
        return hash(tuple(self.dict()))


class ClassificationLabel(Label):
    label: str

    def included(self, labels: Iterable[str]) -> bool:
        return self.label in labels

    def replace(self, mapping: Dict[str, str]) -> 'Label':
        label = mapping.get(self.label, self.label)
        return ClassificationLabel(label=label)

    def overlap_with(self, other) -> bool:
        return self.label == other.label


class SequenceLabel(Label):
    label: str
    start_offset: int
    end_offset: int

    def included(self, labels: Iterable[str]) -> bool:
        return self.label in labels

    def replace(self, mapping: Dict[str, str]) -> 'Label':
        label = mapping.get(self.label, self.label)
        return SequenceLabel(
            label=label,
            start_offset=self.start_offset,
            end_offset=self.end_offset
        )

    def overlap_with(self, other) -> bool:
        if other.end_offset <= self.start_offset:
            return False
        if self.end_offset <= other.start_offset:
            return False
        return True


class Seq2seqLabel(Label):
    text: str

    def included(self, labels: Iterable[str]) -> bool:
        return self.text in labels

    def replace(self, mapping: Dict[str, str]) -> 'Label':
        return self

    def overlap_with(self, other) -> bool:
        return self.text == other.text
