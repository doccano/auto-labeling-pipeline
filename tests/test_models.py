import pytest

from auto_labeling_pipeline.models import (AmazonComprehendSentimentRequestModel, CustomRESTRequestModel,
                                           GCPEntitiesRequestModel, RequestModel)
from auto_labeling_pipeline.request import AmazonComprehendSentimentRequest, RESTRequest


def test_custom_rest_request_model_create_rest_request():
    model = CustomRESTRequestModel(
        url='',
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
