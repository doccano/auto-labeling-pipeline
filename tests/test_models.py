import pytest

from auto_labeling_pipeline.models import (AmazonComprehendSentimentRequestModel, CustomRESTRequestModel,
                                           GCPEntitiesRequestModel, RequestModel, RequestModelFactory)
from auto_labeling_pipeline.request import AmazonComprehendSentimentRequest, RESTRequest


def test_custom_rest_request_model_create_rest_request():
    model = CustomRESTRequestModel(
        url='http://www.example.com',
        method='GET',
        params={},
        headers={},
        body={}
    )
    request = model.build()
    assert isinstance(request, RESTRequest)


def test_gcp_entities_request_model_create_rest_request():
    model = GCPEntitiesRequestModel(
        key='lorem',
        type='PLAIN_TEXT',
        language='en'
    )
    request = model.build()
    assert isinstance(request, RESTRequest)


def test_amazon_comprehend_sentiment_request_model_create_sentiment_request():
    model = AmazonComprehendSentimentRequestModel(
        aws_access_key='',
        aws_secret_access_key='',
        region_name='us-east-1',
        language_code='en'
    )
    request = model.build()
    assert isinstance(request, AmazonComprehendSentimentRequest)


def test_request_model_raises_type_error_on_instantiation():
    with pytest.raises(TypeError):
        RequestModel()


def test_request_model_factory_creates_model_correctly():
    model = GCPEntitiesRequestModel(
        key='lorem',
        type='PLAIN_TEXT',
        language='en'
    )
    model_name = model.__repr_name__()
    attributes = model.dict()
    restored_model = RequestModelFactory.create(model_name, attributes)
    assert restored_model == model


def test_request_model_factory_raises_exception_if_model_does_not_exist():
    with pytest.raises(NameError):
        RequestModelFactory.create('NotExistModel', {})
