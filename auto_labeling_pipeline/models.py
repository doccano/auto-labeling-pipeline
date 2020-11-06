from typing import Literal, Optional

from pydantic import BaseModel, SecretStr

from .request import RESTRequest


class RequestModel(BaseModel):

    def build(self):
        raise NotImplementedError


class CustomRESTRequestModel(RequestModel):
    url: str
    method: Literal['GET', 'POST']
    params: Optional[dict]
    headers: Optional[dict]
    body: Optional[dict]

    def build(self):
        return RESTRequest(**self.dict())


class GCPEntitiesRequestModel(RequestModel):
    key: SecretStr = None
    type: Literal['TYPE_UNSPECIFIED', 'PLAIN_TEXT', 'HTML'] = 'TYPE_UNSPECIFIED'
    language: str = 'en'

    def build(self):
        url = 'https://language.googleapis.com/v1/documents:analyzeEntities'
        method = 'POST'
        headers = {'Content-Type': 'application/json'}
        params = {'key': self.key.get_secret_value()}
        body = {
            'document': {
                'type': self.type,
                'language': self.language,
                'content': '{{ text }}'
            }
        }
        return RESTRequest(url=url, method=method, headers=headers, params=params, body=body)
