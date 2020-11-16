import abc
from typing import Dict, Optional, Set

from auto_labeling_pipeline.labels import Labels


class BasePostProcessor(metaclass=abc.ABCMeta):

    def __init__(self,
                 stop_labels: Optional[Set[str]] = None,
                 mapping: Optional[Dict[str, str]] = None):
        self.stop_labels = stop_labels
        self.mapping = mapping

    @abc.abstractmethod
    def transform(self, labels: Labels) -> Labels:
        raise NotImplementedError


class PostProcessor(BasePostProcessor):

    def transform(self, labels: Labels) -> Labels:
        labels = labels.filter_by_name(self.stop_labels)
        labels = labels.replace_label(self.mapping)
        return labels
