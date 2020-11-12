import os

import vcr

from auto_labeling_pipeline.models import AmazonComprehendSentimentRequestModel, GCPEntitiesRequestModel


def test_gcp_entities_request(cassettes_path):
    with vcr.use_cassette(str(cassettes_path / 'gcp_entities.yaml'), mode='once', filter_query_parameters=['key']):
        model = GCPEntitiesRequestModel(key=os.environ.get('API_KEY_GCP', ''), type='PLAIN_TEXT', language='en')
        request = model.build()
        response = request.send(text='Google, headquartered in Mountain View')
        assert 'entities' in response


def test_amazon_comprehend_sentiment_request(cassettes_path):
    with vcr.use_cassette(str(cassettes_path / 'amazon_comprehend_sentiment.yaml'),
                          mode='once',
                          filter_headers=['authorization']):
        model = AmazonComprehendSentimentRequestModel(
            aws_access_key=os.environ.get('AWS_ACCESS_KEY', ''),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', ''),
            region_name='us-east-1',
            language_code='en'
        )
        request = model.build()
        response = request.send(text='I am very sad.')
        assert 'Sentiment' in response
