import abc
from typing import Dict, Set

from pydantic import BaseModel


class Label(BaseModel, abc.ABC):

    @abc.abstractmethod
    def included(self, labels: Set[str]) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def replace(self, mapping: Dict[str, str]):
        raise NotImplementedError


class ClassificationLabel(Label):
    label: str

    def included(self, labels: Set[str]) -> bool:
        return self.label in labels

    def replace(self, mapping: Dict[str, str]):
        self.label = mapping.get(self.label, self.label)


class SequenceLabel(Label):
    label: str
    start_offset: int
    end_offset: int

    def included(self, labels: Set[str]) -> bool:
        return self.label in labels

    def replace(self, mapping: Dict[str, str]):
        self.label = mapping.get(self.label, self.label)


class Seq2seqLabel(Label):
    text: str

    def included(self, labels: Set[str]) -> bool:
        return self.text in labels

    def replace(self, mapping: Dict[str, str]):
        pass
