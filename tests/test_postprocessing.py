from auto_labeling_pipeline.postprocessing import PostProcessor


def test_postprocessor():
    annotations = [
        {'label': 'PERSON'},
        {'label': 'ORG'},
        {'label': 'Facility'}
    ]
    stop_labels = {'PERSON'}
    mapping = {'Facility': 'ORG'}
    processor = PostProcessor(stop_labels=stop_labels, mapping=mapping)
    processed = processor.transform(annotations)
    expected = [
        {'label': 'ORG'},
        {'label': 'ORG'}
    ]
    assert processed == expected
