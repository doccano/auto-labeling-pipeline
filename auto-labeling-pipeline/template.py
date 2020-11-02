import abc


class Template(metaclass=abc.ABCMeta):
    template_name = None

    def __init__(self, **kwargs):
        pass

    def build(self):
        raise NotImplementedError
