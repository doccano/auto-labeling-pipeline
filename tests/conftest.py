import pathlib

import pytest


@pytest.fixture
def data_path():
    return pathlib.Path(__file__).parent / 'data'
