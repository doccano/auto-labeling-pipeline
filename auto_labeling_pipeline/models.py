import abc
from typing import Dict, Literal, Optional, Type

from pydantic import BaseModel, HttpUrl

from auto_labeling_pipeline.request import AmazonComprehendSentimentRequest, Request, RESTRequest


class RequestModel(BaseModel, abc.ABC):

    @abc.abstractmethod
    def build(self) -> Request:
        raise NotImplementedError


class RequestModelFactory:

    @classmethod
    def create(cls, model_name: str, attributes: Dict) -> RequestModel:
        subclass = cls.find(model_name)
        model = subclass(**attributes)
        return model

    @classmethod
    def find(cls, model_name: str) -> Type[RequestModel]:
        for subclass in RequestModel.__subclasses__():
            if subclass.__name__ == model_name:
                return subclass
        raise NameError(f'{model_name} is not found.')


class CustomRESTRequestModel(RequestModel):
    url: HttpUrl
    method: Literal['GET', 'POST']
    params: Optional[dict]
    headers: Optional[dict]
    body: Optional[dict]

    def build(self) -> Request:
        return RESTRequest(**self.dict())


class GCPEntitiesRequestModel(RequestModel):
    key: str
    type: Literal['TYPE_UNSPECIFIED', 'PLAIN_TEXT', 'HTML']
    language: Literal['zh', 'zh-Hant', 'en', 'fr', 'de', 'it', 'ja', 'ko', 'pt', 'ru', 'es']

    def build(self) -> Request:
        url = 'https://language.googleapis.com/v1/documents:analyzeEntities'
        method = 'POST'
        headers = {'Content-Type': 'application/json'}
        params = {'key': self.key}
        body = {
            'document': {
                'type': self.type,
                'language': self.language,
                'content': '{{ text }}'
            },
            'encodingType': 'UTF32'
        }
        return RESTRequest(url=url, method=method, headers=headers, params=params, body=body)


class AmazonComprehendSentimentRequestModel(RequestModel):
    aws_access_key: str
    aws_secret_access_key: str
    region_name: Literal['us-east-2', 'us-east-1', 'us-west-2', 'ap-south-1', 'ap-northeast-2', 'ap-southeast-1',
                         'ap-southeast-2', 'ap-northeast-1', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2',
                         'us-gov-west-1']
    language_code: Literal['en', 'es', 'fr', 'de', 'it', 'pt', 'ar', 'hi', 'ja', 'ko', 'zh', 'zh-TW']

    def build(self) -> Request:
        return AmazonComprehendSentimentRequest(
            aws_access_key=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
            language_code=self.language_code
        )
