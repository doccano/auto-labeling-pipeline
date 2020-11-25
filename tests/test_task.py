import pytest

from auto_labeling_pipeline.label import ClassificationLabel, Seq2seqLabel, SequenceLabel
from auto_labeling_pipeline.labels import ClassificationLabels, Seq2seqLabels, SequenceLabels
from auto_labeling_pipeline.task import Task


@pytest.mark.parametrize(
    'name, expected',
    [
        ('TextClassification', ClassificationLabel),
        ('SequenceLabeling', SequenceLabel),
        ('Seq2seq', Seq2seqLabel)
    ]
)
def test_return_correct_label_class(name, expected):
    task = Task(name)
    label_class = task.label_class
    assert label_class == expected


@pytest.mark.parametrize(
    'name, expected',
    [
        ('TextClassification', ClassificationLabels),
        ('SequenceLabeling', SequenceLabels),
        ('Seq2seq', Seq2seqLabels)
    ]
)
def test_return_correct_label_collection(name, expected):
    task = Task(name)
    label_collection = task.label_collection
    assert label_collection == expected
