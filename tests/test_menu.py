import pytest

from auto_labeling_pipeline.menu import Options
from auto_labeling_pipeline.task import DocumentClassification, GenericTask


@pytest.mark.parametrize(
    'task, expected',
    [
        ('DocumentClassification', {GenericTask, DocumentClassification}),
        ('XXX', {GenericTask})
    ]
)
def test_filter_task(task, expected):
    options = Options.filter_by_task(task_name=task)
    tasks = {o.task for o in options}
    assert tasks == expected


@pytest.mark.parametrize(
    'option_name',
    [
        'Custom REST Request',
        'Amazon Comprehend Sentiment Analysis',
        'GCP Entity Analysis'
    ]
)
def test_find_option(option_name):
    option = Options.find(option_name)
    assert option.name == option_name


def test_find_invalid_option():
    with pytest.raises(ValueError):
        Options.find('XXX')
