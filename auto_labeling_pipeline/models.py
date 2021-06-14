import abc
import base64
from typing import Dict, Optional, Type

import boto3
import requests
from pydantic import AnyHttpUrl, BaseModel
from typing_extensions import Literal


class RequestModel(BaseModel, abc.ABC):

    @abc.abstractmethod
    def send(self, text: str):
        raise NotImplementedError


class RequestModelFactory:

    @classmethod
    def create(cls, model_name: str, attributes: Dict) -> RequestModel:
        subclass = cls.find(model_name)
        model = subclass(**attributes)
        return model

    @classmethod
    def find(cls, model_name: str) -> Type[RequestModel]:
        def get_all_subclasses(cls):
            all_subclasses = []
            for subclass in cls.__subclasses__():
                all_subclasses.append(subclass)
                all_subclasses.extend(get_all_subclasses(subclass))
            return all_subclasses

        for subclass in get_all_subclasses(RequestModel):
            if subclass.Config.title == model_name:
                return subclass
        raise NameError(f'{model_name} is not found.')


def find_and_replace_value(obj, value, target='{{ text }}'):
    for k, v in obj.items():
        if v == target:
            obj[k] = value
            return
        if isinstance(v, dict):
            find_and_replace_value(v, value, target)


class CustomRESTRequestModel(RequestModel):
    """
    This allow you to call any REST API.
    """
    url: AnyHttpUrl
    method: Literal['GET', 'POST']
    params: Optional[dict]
    headers: Optional[dict]
    body: Optional[dict]

    class Config:
        title = 'Custom REST Request'

    def send(self, text: str):
        find_and_replace_value(self.body, text)
        find_and_replace_value(self.params, text)
        response = requests.request(
            url=self.url,
            method=self.method,
            params=self.params,
            headers=self.headers,
            json=self.body
        ).json()
        return response


class GCPEntitiesRequestModel(RequestModel):
    """
    This allow you to analyze entities in a text by
    <a href="https://cloud.google.com/natural-language/docs/analyzing-entities">Cloud Natural Language API</a>.
    """
    key: str
    type: Literal['TYPE_UNSPECIFIED', 'PLAIN_TEXT', 'HTML']
    language: Literal['zh', 'zh-Hant', 'en', 'fr', 'de', 'it', 'ja', 'ko', 'pt', 'ru', 'es']

    class Config:
        title = 'GCP Entity Analysis'
        schema_extra = {
            # https://cloud.google.com/natural-language/docs/reference/rest/v1/Entity#Type
            'types': [
                'UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION', 'EVENT', 'WORK_OF_ART',
                'CONSUMER_GOOD', 'OTHER', 'PHONE_NUMBER', 'ADDRESS', 'DATE', 'NUMBER', 'PRICE'
            ]
        }

    def send(self, text: str):
        url = 'https://language.googleapis.com/v1/documents:analyzeEntities'
        headers = {'Content-Type': 'application/json'}
        params = {'key': self.key}
        body = {
            'document': {
                'type': self.type,
                'language': self.language,
                'content': text
            },
            'encodingType': 'UTF32'
        }
        response = requests.post(url, headers=headers, params=params, json=body).json()
        return response


class AWSMixin(BaseModel):
    aws_access_key: str
    aws_secret_access_key: str
    region_name: Literal[
        'us-east-1',
        'us-east-2',
        'us-west-2',
        'us-gov-west-1',
        'ap-south-1',
        'ap-southeast-1',
        'ap-southeast-2',
        'ap-northeast-1',
        'ap-northeast-2',
        'ca-central-1',
        'eu-central-1',
        'eu-west-1',
        'eu-west-2',
    ]


class AmazonComprehendRequestModel(AWSMixin, RequestModel):
    language_code: Literal['en', 'es', 'fr', 'de', 'it', 'pt', 'ar', 'hi', 'ja', 'ko', 'zh', 'zh-TW']

    @property
    def client(self):
        return boto3.client(
            'comprehend',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )

    def send(self, text: str):
        raise NotImplementedError('Please use the subclass.')


class AmazonComprehendSentimentRequestModel(AmazonComprehendRequestModel):
    """
    This allow you to determine the sentiment of a text by
    <a href="https://docs.aws.amazon.com/en_us/comprehend/">Amazon Comprehend</a>.
    """

    class Config:
        title = 'Amazon Comprehend Sentiment Analysis'
        schema_extra = {
            # https://docs.aws.amazon.com/comprehend/latest/dg/how-sentiment.html
            'types': [
                'POSITIVE', 'NEGATIVE', 'NEUTRAL', 'MIXED'
            ]
        }

    def send(self, text: str):
        response = self.client.detect_sentiment(
            Text=text,
            LanguageCode=self.language_code
        )
        return response


class AmazonComprehendEntityRequestModel(AmazonComprehendRequestModel):
    """
    This allow you to detect entities in the text by
    <a href="https://docs.aws.amazon.com/en_us/comprehend/">Amazon Comprehend</a>.
    """

    class Config:
        title = 'Amazon Comprehend Entity Recognition'
        schema_extra = {
            # https://docs.aws.amazon.com/comprehend/latest/dg/how-entities.html
            'types': [
                'PERSON', 'LOCATION', 'ORGANIZATION', 'COMMERCIAL_ITEM',
                'EVENT', 'DATE', 'QUANTITY', 'TITLE', 'OTHER'
            ]
        }

    def send(self, text: str):
        response = self.client.detect_entities(
            Text=text,
            LanguageCode=self.language_code
        )
        return response


class AmazonComprehendPIIEntityRequestModel(AmazonComprehendRequestModel):
    """
    This allow you to detect PII entities in the text by
    <a href="https://docs.aws.amazon.com/en_us/comprehend/">Amazon Comprehend</a>.
    """
    language_code: Literal['en']

    class Config:
        title = 'Amazon Comprehend PII Entity Recognition'
        schema_extra = {
            # https://docs.aws.amazon.com/comprehend/latest/dg/how-pii.html
            'types': [
                'BANK_ACCOUNT_NUMBER', 'BANK_ROUTING', 'CREDIT_DEBIT_NUMBER',
                'CREDIT_DEBIT_CVV', 'CREDIT_DEBIT_EXPIRY', 'PIN', 'EMAIL',
                'ADDRESS', 'NAME', 'PHONE', 'SSN', 'DATE_TIME', 'PASSPORT_NUMBER',
                'DRIVER_ID', 'URL', 'AGE', 'USERNAME', 'PASSWORD', 'AWS_ACCESS_KEY',
                'AWS_SECRET_KEY', 'IP_ADDRESS', 'MAC_ADDRESS', 'ALL'
            ]
        }

    def send(self, text: str):
        response = self.client.detect_pii_entities(
            Text=text,
            LanguageCode=self.language_code
        )
        return response


class GCPImageLabelDetectionRequestModel(RequestModel):
    """
    This allow you to detect labels for a image by
    <a href="https://cloud.google.com/vision/docs/labels">Cloud Vision API</a>.
    """
    key: str

    class Config:
        title = 'GCP Image Label Detection'

    def send(self, filepath: str):
        url = 'https://vision.googleapis.com/v1/images:annotate'
        headers = {'Content-Type': 'application/json'}
        params = {'key': self.key}
        body = {
            'requests': [
                {
                    'image': {
                        'content': load_image_as_b64(filepath)
                    },
                    'features': [
                        {
                            'maxResults': 5,
                            'type': 'LABEL_DETECTION'
                        }
                    ]
                }
            ]
        }
        response = requests.post(url, headers=headers, params=params, json=body).json()
        return response


class AmazonRekognitionLabelDetectionRequestModel(AWSMixin, RequestModel):
    """
    This allow you to detect labels for a image by Amazon Rekognition.
    """
    class Config:
        title = 'Amazon Rekognition Label Detection'

    @property
    def client(self):
        return boto3.client(
            'rekognition',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )

    def send(self, filepath: str):
        with open(filepath, 'rb') as f:
            response = self.client.detect_labels(
                Image={'Bytes': f.read()},
            )
            return response


def load_image_as_b64(filepath):
    with open(filepath, 'rb') as f:
        b64_image = base64.b64encode(f.read())
        return b64_image.decode('utf-8')
