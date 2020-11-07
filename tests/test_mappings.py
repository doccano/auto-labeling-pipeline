from auto_labeling_pipeline.mappings import MappingTemplate


def test_amazon_comprehend_sentiment():
    response = {
        'Sentiment': 'POSITIVE',
        'SentimentScore': {
            'Positive': 0,
            'Negative': 0,
            'Neutral': 0,
            'Mixed': 0
        }
    }
    template = '[{"label": "{{ input.Sentiment }}"}]'
    mapping_template = MappingTemplate(template)
    annotations = mapping_template.render(response)
    expected = [{'label': 'POSITIVE'}]
    assert annotations == expected

