from typing import Literal

from pydantic import BaseModel, SecretStr

from .request import GCPEntitiesRequest


class RequestModel(BaseModel):

    def build(self):
        raise NotImplementedError


class GCPEntitiesRequestModel(RequestModel):
    key: SecretStr = None
    type: Literal['TYPE_UNSPECIFIED', 'PLAIN_TEXT', 'HTML'] = 'TYPE_UNSPECIFIED'
    language: str = 'en'

    def build(self):
        return GCPEntitiesRequest(key=self.key.get_secret_value(), type=self.type, language=self.language)
