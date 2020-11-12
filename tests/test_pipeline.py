import os

import vcr

from auto_labeling_pipeline.mappings import AmazonComprehendSentimentTemplate
from auto_labeling_pipeline.models import AmazonComprehendSentimentRequestModel
from auto_labeling_pipeline.pipeline import pipeline
from auto_labeling_pipeline.postprocessing import PostProcessor


def test_amazon_pipeline(cassettes_path):
    with vcr.use_cassette(str(cassettes_path / 'amazon_comprehend_sentiment.yaml'),
                          mode='once',
                          filter_headers=['authorization']):
        model = AmazonComprehendSentimentRequestModel(
            aws_access_key=os.environ.get('AWS_ACCESS_KEY', ''),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', ''),
            region_name='us-east-1',
            language_code='en'
        )
        template = AmazonComprehendSentimentTemplate()
        post_processor = PostProcessor()
        labels = pipeline(
            text='I am very sad.',
            request_model=model,
            mapping_template=template,
            post_processing=post_processor
        )
        labels = labels.dict()
        assert isinstance(labels, list)
        assert len(labels) == 1
        assert 'label' in labels[0]
