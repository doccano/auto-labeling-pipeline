from auto_labeling_pipeline.label import ClassificationLabel
from auto_labeling_pipeline.labels import ClassificationLabels
from auto_labeling_pipeline.postprocessing import PostProcessor


def test_postprocessor():
    labels = [
        {'label': 'PERSON'},
        {'label': 'ORG'},
        {'label': 'Facility'}
    ]
    labels = [ClassificationLabel(**label) for label in labels]
    labels = ClassificationLabels(labels)
    stop_labels = {'PERSON'}
    mapping = {'Facility': 'ORG'}
    processor = PostProcessor(stop_labels=stop_labels, mapping=mapping)
    labels = processor.transform(labels).dict()
    expected = [
        {'label': 'ORG'},
        {'label': 'ORG'}
    ]
    assert labels == expected
