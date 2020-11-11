import json

from auto_labeling_pipeline.mappings import AmazonComprehendSentimentTemplate, GCPEntitiesTemplate


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
