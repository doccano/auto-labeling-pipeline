import json

from auto_labeling_pipeline.mappings import (AmazonComprehendEntityTemplate, AmazonComprehendSentimentTemplate,
                                             AmazonRekognitionLabelDetectionTemplate, GCPEntitiesTemplate,
                                             GCPImageLabelDetectionTemplate)


def load_json(filepath):
    with open(filepath) as f:
        return json.load(f)


def test_amazon_comprehend_sentiment(data_path):
    response = load_json(data_path / 'amazon_comprehend_sentiment.json')
    mapping_template = AmazonComprehendSentimentTemplate()
    labels = mapping_template.render(response)
    labels = labels.dict()
    expected = [{'label': 'NEUTRAL'}]
    assert labels == expected


def test_gcp_entities(data_path):
    response = load_json(data_path / 'gcp_entities.json')
    mapping_template = GCPEntitiesTemplate()
    labels = mapping_template.render(response)
    labels = labels.dict()
    expected = [
        {
            'label': 'PERSON',
            'start_offset': 10,
            'end_offset': 15
        },
        {
            'label': 'LOCATION',
            'start_offset': 36,
            'end_offset': 47
        },
        {
            'label': 'LOCATION',
            'start_offset': 65,
            'end_offset': 84
        },
        {
            'label': 'LOCATION',
            'start_offset': 86,
            'end_offset': 100
        },
        {
            'label': 'ADDRESS',
            'start_offset': 60,
            'end_offset': 100
        },
        {
            'label': 'NUMBER',
            'start_offset': 60,
            'end_offset': 64
        },
        {
            'label': 'DATE',
            'start_offset': 105,
            'end_offset': 114
        },
        {
            'label': 'NUMBER',
            'start_offset': 113,
            'end_offset': 114
        },
    ]
    assert labels == expected


def test_amazon_comprehend_entities(data_path):
    response = load_json(data_path / 'amazon_comprehend_entity.json')
    template = AmazonComprehendEntityTemplate()
    labels = template.render(response)
    labels = labels.dict()
    expected = [
        {
            'label': 'DATE',
            'start_offset': 14,
            'end_offset': 19
        },
        {
            'label': 'LOCATION',
            'start_offset': 23,
            'end_offset': 30
        }
    ]
    assert labels == expected


def test_gcp_image_label_detection(data_path):
    response = load_json(data_path / 'gcp_image_label_detection.json')
    template = GCPImageLabelDetectionTemplate()
    labels = template.render(response)
    labels = labels.dict()
    expected = [{'label': 'Cat'}]
    assert labels == expected


def test_aws_image_label_detection(data_path):
    response = load_json(data_path / 'amazon_rekognition_label_detection.json')
    template = AmazonRekognitionLabelDetectionTemplate()
    labels = template.render(response)
    labels = labels.dict()
    expected = [{'label': 'Cat'}]
    assert labels == expected
