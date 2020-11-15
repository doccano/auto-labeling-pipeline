import pytest

from auto_labeling_pipeline.label import ClassificationLabel, Seq2seqLabel, SequenceLabel
from auto_labeling_pipeline.labels import ClassificationLabels, Seq2seqLabels, SequenceLabels


@pytest.fixture
def example_classification_data():
    labels = [
        {'label': 'A'},
        {'label': 'B'},
        {'label': 'C'}
    ]
    labels = [ClassificationLabel(**label) for label in labels]
    labels = ClassificationLabels(labels)
    return labels


@pytest.fixture
def example_sequence_data():
    labels = [
        {'label': 'A', 'start_offset': 0, 'end_offset': 1},
        {'label': 'B', 'start_offset': 1, 'end_offset': 2},
        {'label': 'C', 'start_offset': 2, 'end_offset': 3}
    ]
    labels = [SequenceLabel(**label) for label in labels]
    labels = SequenceLabels(labels)
    return labels


@pytest.fixture
def example_seq2seq_data():
    labels = [
        {'text': 'A'},
        {'text': 'B'},
        {'text': 'C'}
    ]
    labels = [Seq2seqLabel(**label) for label in labels]
    labels = Seq2seqLabels(labels)
    return labels


class TestClassificationLabels:

    def test_filter_by_name(self, example_classification_data):
        stop_labels = {'B', 'C', 'D'}
        labels = example_classification_data.filter_by_name(stop_labels)
        labels = labels.dict()
        expected = [
            {'label': 'A'}
        ]
        assert labels == expected

    def test_dont_filter_by_name(self, example_classification_data):
        labels = example_classification_data.filter_by_name()
        assert labels == example_classification_data

    def test_convert_label(self, example_classification_data):
        mapping = {'C': 'D'}
        labels = example_classification_data.replace_label(mapping)
        labels = labels.dict()
        expected = [
            {'label': 'A'},
            {'label': 'B'},
            {'label': 'D'}
        ]
        assert labels == expected

    def test_dont_convert_label(self, example_classification_data):
        labels = example_classification_data.replace_label()
        assert labels == example_classification_data


class TestSequenceLabels:

    def test_filter_by_name(self, example_sequence_data):
        stop_labels = {'B', 'C', 'D'}
        labels = example_sequence_data.filter_by_name(stop_labels)
        labels = labels.dict()
        expected = [
            {'label': 'A', 'start_offset': 0, 'end_offset': 1}
        ]
        assert labels == expected

    def test_dont_filter_by_name(self, example_sequence_data):
        labels = example_sequence_data.filter_by_name()
        assert labels == example_sequence_data

    def test_convert_label(self, example_sequence_data):
        mapping = {'C': 'D'}
        labels = example_sequence_data.replace_label(mapping)
        labels = labels.dict()
        expected = [
            {'label': 'A', 'start_offset': 0, 'end_offset': 1},
            {'label': 'B', 'start_offset': 1, 'end_offset': 2},
            {'label': 'D', 'start_offset': 2, 'end_offset': 3}
        ]
        assert labels == expected

    def test_dont_convert_label(self, example_sequence_data):
        labels = example_sequence_data.replace_label()
        assert labels == example_sequence_data


class TestSeq2seqLabels:

    def test_filter_by_name(self, example_seq2seq_data):
        stop_labels = {'B', 'C', 'D'}
        labels = example_seq2seq_data.filter_by_name(stop_labels)
        assert labels == example_seq2seq_data

    def test_convert_label(self, example_seq2seq_data):
        mapping = {'C': 'D'}
        labels = example_seq2seq_data.replace_label(mapping)
        assert labels == example_seq2seq_data
