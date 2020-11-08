from auto_labeling_pipeline.mappings import AmazonComprehendSentimentTemplate


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
    mapping_template = AmazonComprehendSentimentTemplate()
    annotations = mapping_template.render(response)
    expected = [{'label': 'POSITIVE'}]
    assert annotations == expected

