from auto_labeling_pipeline.label import ClassificationLabel
from auto_labeling_pipeline.labels import ClassificationLabels
from auto_labeling_pipeline.postprocessing import PostProcessor


def test_postprocessor():
    annotations = [
        {'label': 'PERSON'},
        {'label': 'ORG'},
        {'label': 'Facility'}
    ]
    annotations = [ClassificationLabel(**label) for label in annotations]
    annotations = ClassificationLabels(annotations)
    stop_labels = {'PERSON'}
    mapping = {'Facility': 'ORG'}
    processor = PostProcessor(stop_labels=stop_labels, mapping=mapping)
    processed = processor.transform(annotations)
    expected = [
        {'label': 'ORG'},
        {'label': 'ORG'}
    ]
    labels = processed.dict()
    assert labels == expected
