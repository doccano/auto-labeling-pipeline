from auto_labeling_pipeline.labels import ClassificationLabels
from auto_labeling_pipeline.postprocessing import PostProcessor


def test_postprocessor():
    labels = [
        {'label': 'PERSON'},
        {'label': 'ORG'},
        {'label': 'Facility'}
    ]
    labels = ClassificationLabels(labels)
    mapping = {'Facility': 'ORG'}
    processor = PostProcessor(mapping=mapping)
    labels = processor.transform(labels).dict()
    expected = [
        {'label': 'ORG'},
    ]
    assert labels == expected


def test_to_dict():
    expected = {'Facility': 'ORG'}
    processor = PostProcessor(mapping=expected)
    actual = processor.to_dict()
    assert actual == expected


def test_load():
    expected = {'Facility': 'ORG'}
    processor = PostProcessor.load(mapping=expected)
    actual = processor.mapping
    assert actual == expected
