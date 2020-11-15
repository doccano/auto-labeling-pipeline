import abc
from typing import Set

from pydantic import BaseModel


class Label(BaseModel, abc.ABC):

    @abc.abstractmethod
    def included(self, labels: Set[str]) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def replace(self, mapping: dict):
        raise NotImplementedError


class ClassificationLabel(Label):
    label: str

    def included(self, labels: Set[str]) -> bool:
        return self.label in labels

    def replace(self, mapping: dict):
        if self.label in mapping:
            self.label = mapping[self.label]


class SequenceLabel(Label):
    label: str
    start_offset: int
    end_offset: int

    def included(self, labels: Set[str]) -> bool:
        return self.label in labels

    def replace(self, mapping: dict):
        if self.label in mapping:
            self.label = mapping[self.label]


class Seq2seqLabel(Label):
    text: str

    def included(self, labels: Set[str]) -> bool:
        return self.text in labels

    def replace(self, mapping: dict):
        pass
