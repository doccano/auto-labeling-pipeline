import abc

import requests


class Request(metaclass=abc.ABCMeta):

    def __init__(self, **kwargs):
        pass

    def send(self, text):
        raise NotImplementedError


class CustomRequest(Request):

    def __init__(self, **kwargs):
        super().__init__()
        self.url = kwargs['url']
        self.params = kwargs['params']
        self.method = kwargs['method']
        self.body = kwargs['body']
        self.headers = kwargs['headers']

    def send(self, text):
        response = requests.request(
            url=self.url,
            method=self.method,
            params=self.params,
            headers=self.headers,
            data=self.body
        ).json()
        return response


class GCPEntitiesRequest(Request):

    def __init__(self, **kwargs):
        super().__init__()
        self.key = kwargs['key']
        self.language = kwargs['language']
        self.type = kwargs['type']

    def send(self, text):
        url = 'https://language.googleapis.com/v1/documents:analyzeEntities?key={}'.format(self.key)
        headers = {'Content-Type': 'application/json'}
        body = {
            'document': {
                'type': self.type,
                'language': self.language,
                'content': text
            }
        }
        response = requests.post(url, headers=headers, json=body).json()
        return response
