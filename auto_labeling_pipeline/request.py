import abc

import boto3
import requests


def find_and_replace_value(obj, value, target='{{ text }}'):
    for k, v in obj.items():
        if v == target:
            obj[k] = value
            return
        if isinstance(v, dict):
            find_and_replace_value(v, value, target)


class Request(abc.ABC):

    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    def send(self, text: str):
        raise NotImplementedError


class RESTRequest(Request):

    def __init__(self, **kwargs):
        super().__init__()
        self.url = kwargs['url']
        self.params = kwargs['params']
        self.method = kwargs['method']
        self.body = kwargs['body']
        self.headers = kwargs['headers']

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


class AmazonComprehendRequest(Request):

    def __init__(self, **kwargs):
        super().__init__()
        self.comprehend = boto3.client(
            'comprehend',
            aws_access_key_id=kwargs['aws_access_key'],
            aws_secret_access_key=kwargs['aws_secret_access_key'],
            region_name=kwargs['region_name']
        )
        self.language_code = kwargs['language_code']

    def send(self, text: str):
        pass


class AmazonComprehendSentimentRequest(AmazonComprehendRequest):

    def send(self, text: str):
        response = self.comprehend.detect_sentiment(Text=text, LanguageCode=self.language_code)
        return response
