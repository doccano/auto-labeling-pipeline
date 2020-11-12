import pathlib

import pytest


@pytest.fixture
def data_path():
    return pathlib.Path(__file__).parent / 'data'


@pytest.fixture
def cassettes_path():
    return pathlib.Path(__file__).parent / 'fixtures/cassettes'
