import pytest

from auto_labeling_pipeline.labels import ClassificationLabels, Seq2seqLabels, SequenceLabels
from auto_labeling_pipeline.task import DocumentClassification, ImageClassification, Seq2seq, SequenceLabeling


@pytest.mark.parametrize(
    'task, expected',
    [
        (DocumentClassification, ClassificationLabels),
        (SequenceLabeling, SequenceLabels),
        (Seq2seq, Seq2seqLabels),
        (ImageClassification, ClassificationLabels)
    ]
)
def test_return_correct_label_collection(task, expected):
    assert task.label_collection == expected
