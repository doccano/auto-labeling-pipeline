import abc


class Request(metaclass=abc.ABCMeta):

    def __init__(self, **kwargs):
        pass

    def send(self):
        raise NotImplementedError
