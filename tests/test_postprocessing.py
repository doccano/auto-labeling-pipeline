from auto_labeling_pipeline.label import ClassificationLabel
from auto_labeling_pipeline.postprocessing import ClassificationPostProcessor


def test_postprocessor():
    annotations = [
        {'label': 'PERSON'},
        {'label': 'ORG'},
        {'label': 'Facility'}
    ]
    annotations = [ClassificationLabel(**label) for label in annotations]
    stop_labels = {'PERSON'}
    mapping = {'Facility': 'ORG'}
    processor = ClassificationPostProcessor(stop_labels=stop_labels, mapping=mapping)
    processed = processor.transform(annotations)
    expected = [
        {'label': 'ORG'},
        {'label': 'ORG'}
    ]
    assert processed == expected
