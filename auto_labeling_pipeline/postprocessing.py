import abc
from typing import Optional, Set

from auto_labeling_pipeline.labels import Labels


class PostProcessor(metaclass=abc.ABCMeta):

    def __init__(self, stop_labels: Optional[Set] = None, mapping: Optional[dict] = None):
        self.stop_labels = stop_labels
        self.mapping = mapping

    def transform(self, annotations: Labels) -> Labels:
        annotations = annotations.filter_by_name(self.stop_labels)
        annotations = annotations.convert_label(self.mapping)
        return annotations
