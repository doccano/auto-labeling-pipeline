import abc
from typing import Literal, Optional

from pydantic import BaseModel

from auto_labeling_pipeline.request import AmazonComprehendSentimentRequest, Request, RESTRequest


class RequestModel(BaseModel, abc.ABC):

    @abc.abstractmethod
    def build(self) -> Request:
        raise NotImplementedError


class CustomRESTRequestModel(RequestModel):
    url: str
    method: Literal['GET', 'POST']
    params: Optional[dict]
    headers: Optional[dict]
    body: Optional[dict]

    def build(self) -> Request:
        return RESTRequest(**self.dict())


class GCPEntitiesRequestModel(RequestModel):
    key: str
    type: Literal['TYPE_UNSPECIFIED', 'PLAIN_TEXT', 'HTML'] = 'TYPE_UNSPECIFIED'
    language: str = 'en'

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
            }
        }
        return RESTRequest(url=url, method=method, headers=headers, params=params, body=body)


class AmazonComprehendSentimentRequestModel(RequestModel):
    aws_access_key: str
    aws_secret_access_key: str
    region_name: str
    language_code: str

    def build(self) -> Request:
        return AmazonComprehendSentimentRequest(
            aws_access_key=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
            language_code=self.language_code
        )
