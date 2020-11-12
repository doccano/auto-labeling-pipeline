import os

import vcr

from auto_labeling_pipeline.models import GCPEntitiesRequestModel


def test_gcp_entities_request(cassettes_path):
    with vcr.use_cassette(str(cassettes_path / 'gcp_entities.yaml'), mode='once', filter_query_parameters=['key']):
        model = GCPEntitiesRequestModel(key=os.environ.get('API_KEY_GCP', ''), type='PLAIN_TEXT', language='en')
        request = model.build()
        response = request.send(text='Google, headquartered in Mountain View')
        assert 'entities' in response
