class PostProcessor:

    def __init__(self, stop_labels=None, mapping=None):
        self.stop_labels = stop_labels
        self.mapping = mapping

    def transform(self, annotations):
        annotations = self.filter_by_label(annotations)
        annotations = self.convert_label(annotations)
        return annotations

    def filter_by_label(self, annotations):
        if not self.stop_labels:
            return annotations
        return [a for a in annotations if a['label'] not in self.stop_labels]

    def convert_label(self, annotations):
        if not self.mapping:
            return annotations
        for a in annotations:
            label = a['label']
            if label in self.mapping:
                a['label'] = self.mapping[label]
        return annotations
