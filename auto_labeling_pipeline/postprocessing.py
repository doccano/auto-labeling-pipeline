import abc
from typing import Dict

from auto_labeling_pipeline.labels import Labels


class BasePostProcessor(abc.ABC):

    def __init__(self, mapping: Dict[str, str]):
        self.mapping = mapping

    @abc.abstractmethod
    def transform(self, labels: Labels) -> Labels:
        raise NotImplementedError

    def to_dict(self) -> Dict[str, str]:
        return self.mapping

    @classmethod
    def load(cls, mapping: Dict[str, str]) -> 'BasePostProcessor':
        return cls(mapping=mapping)


class PostProcessor(BasePostProcessor):

    def transform(self, labels: Labels) -> Labels:
        labels = labels.filter_by_name(self.mapping)
        labels = labels.replace_label(self.mapping)
        labels = labels.remove_overlapping()
        return labels
