import os

import pytest
import vcr

from auto_labeling_pipeline.models import (AmazonComprehendSentimentRequestModel,
                                           AmazonRekognitionLabelDetectionRequestModel, GCPEntitiesRequestModel,
                                           GCPImageLabelDetectionRequestModel, RequestModel, RequestModelFactory,
                                           load_image_as_b64)


def test_find_model():
    model = RequestModelFactory.find('Amazon Comprehend Sentiment Analysis')
    assert model == AmazonComprehendSentimentRequestModel


def test_request_model_raises_type_error_on_instantiation():
    with pytest.raises(TypeError):
        RequestModel()


def test_request_model_factory_creates_model_correctly():
    model = GCPEntitiesRequestModel(
        key='lorem',
        type='PLAIN_TEXT',
        language='en'
    )
    model_name = model.Config.title
    attributes = model.dict()
    restored_model = RequestModelFactory.create(model_name, attributes)
    assert restored_model == model


def test_request_model_factory_raises_exception_if_model_does_not_exist():
    with pytest.raises(NameError):
        RequestModelFactory.create('NotExistModel', {})


def test_gcp_entities_request(cassettes_path):
    with vcr.use_cassette(str(cassettes_path / 'gcp_entities.yaml'), mode='once', filter_query_parameters=['key']):
        model = GCPEntitiesRequestModel(key=os.environ.get('API_KEY_GCP', ''), type='PLAIN_TEXT', language='en')
        response = model.send(text='Google, headquartered in Mountain View')
        assert 'entities' in response


def test_gcp_image_label_detection(data_path, cassettes_path):
    with vcr.use_cassette(
            str(cassettes_path / 'gcp_label_detection.yaml'),
            mode='once',
            filter_query_parameters=['key']
    ):
        model = GCPImageLabelDetectionRequestModel(
            key=os.environ.get('API_KEY_GCP', '')
        )
        filepath = data_path / 'images/1500x500.jpeg'
        response = model.send(filepath)
        assert 'responses' in response
        assert 'labelAnnotations' in response['responses'][0]


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
        response = model.send(text='I am very sad.')
        assert 'Sentiment' in response


def test_amazon_rekognition_label_detection(data_path, cassettes_path):
    with vcr.use_cassette(
            str(cassettes_path / 'amazon_rekognition_label_detection.yaml'),
            mode='once',
            filter_headers=['authorization']
    ):
        model = AmazonRekognitionLabelDetectionRequestModel(
            aws_access_key=os.environ.get('AWS_ACCESS_KEY', ''),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', ''),
            region_name='us-east-1',
        )
        filepath = data_path / 'images/1500x500.jpeg'
        response = model.send(filepath)
        assert 'Labels' in response
