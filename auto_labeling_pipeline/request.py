import abc
import json

import requests
from jinja2 import Template


def render(template_str: str, text: str):
    template = Template(template_str)
    return template.render(text=text)


class Request(metaclass=abc.ABCMeta):

    def __init__(self, **kwargs):
        pass

    def send(self, text):
        raise NotImplementedError


class RESTRequest(Request):

    def __init__(self, **kwargs):
        super().__init__()
        self.url = kwargs['url']
        self.params = kwargs['params']
        self.method = kwargs['method']
        self.body = kwargs['body']
        self.headers = kwargs['headers']

    def send(self, text):
        body = render(json.dumps(self.body), text)
        params = render(json.dumps(self.params), text)
        response = requests.request(
            url=self.url,
            method=self.method,
            params=params,
            headers=self.headers,
            data=body
        ).json()
        return response
