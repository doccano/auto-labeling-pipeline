from typing import Literal, Optional

from pydantic import BaseModel, SecretStr

from .request import CustomRESTRequest, GCPEntitiesRequest


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
        return CustomRESTRequest(**self.dict())


class GCPEntitiesRequestModel(RequestModel):
    key: SecretStr = None
    type: Literal['TYPE_UNSPECIFIED', 'PLAIN_TEXT', 'HTML'] = 'TYPE_UNSPECIFIED'
    language: str = 'en'

    def build(self):
        return GCPEntitiesRequest(key=self.key.get_secret_value(), type=self.type, language=self.language)
