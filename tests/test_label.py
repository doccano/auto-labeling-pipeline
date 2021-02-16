import pytest

from auto_labeling_pipeline.label import ClassificationLabel, Seq2seqLabel, SequenceLabel


class TestClassificationLabels:

    @pytest.mark.parametrize(
        'label, labels, expected',
        [
            ('A', {'A'}, True),
            ('A', {'B'}, False)
        ]
    )
    def test_included(self, label, labels, expected):
        label = ClassificationLabel(label=label)
        actual = label.included(labels)
        assert actual == expected

    @pytest.mark.parametrize(
        'label, mapping, expected',
        [
            ('A', {'A': 'B'}, ClassificationLabel(label='B')),
            ('A', {'B': 'B'}, ClassificationLabel(label='A'))
        ]
    )
    def test_replace(self, label, mapping, expected):
        label = ClassificationLabel(label=label)
        label = label.replace(mapping)
        assert label == expected

    @pytest.mark.parametrize(
        'label, other, expected',
        [
            ('A', 'A', True),
            ('A', 'B', False)
        ]
    )
    def test_overlap(self, label, other, expected):
        label = ClassificationLabel(label=label)
        other = ClassificationLabel(label=other)
        actual = label.overlap_with(other)
        assert actual == expected


class TestSequenceLabel:

    @pytest.mark.parametrize(
        'label, other, expected',
        [
            (
                SequenceLabel(label='A', start_offset=0, end_offset=2),
                SequenceLabel(label='A', start_offset=2, end_offset=3),
                False
            ),
            (
                SequenceLabel(label='A', start_offset=2, end_offset=3),
                SequenceLabel(label='A', start_offset=0, end_offset=2),
                False
            ),
            (
                SequenceLabel(label='A', start_offset=0, end_offset=2),
                SequenceLabel(label='A', start_offset=1, end_offset=3),
                True
            ),
            (
                SequenceLabel(label='A', start_offset=0, end_offset=3),
                SequenceLabel(label='A', start_offset=2, end_offset=3),
                True
            ),
            (
                SequenceLabel(label='A', start_offset=2, end_offset=3),
                SequenceLabel(label='A', start_offset=2, end_offset=3),
                True
            )
        ]
    )
    def test_overlap(self, label, other, expected):
        actual = label.overlap_with(other)
        assert actual == expected


class TestSeq2seqLabel:

    @pytest.mark.parametrize(
        'text, labels, expected',
        [
            ('A', {'A'}, True),
            ('A', {'B'}, False)
        ]
    )
    def test_included(self, text, labels, expected):
        label = Seq2seqLabel(text=text)
        actual = label.included(labels)
        assert actual == expected

    @pytest.mark.parametrize(
        'text, mapping, expected',
        [
            ('A', {'A': 'B'}, Seq2seqLabel(text='A')),
            ('A', {'B': 'B'}, Seq2seqLabel(text='A'))
        ]
    )
    def test_replace(self, text, mapping, expected):
        label = Seq2seqLabel(text=text)
        label = label.replace(mapping)
        assert label == expected

    @pytest.mark.parametrize(
        'text, other, expected',
        [
            ('A', 'A', True),
            ('A', 'B', False)
        ]
    )
    def test_overlap(self, text, other, expected):
        label = Seq2seqLabel(text=text)
        other = Seq2seqLabel(text=other)
        actual = label.overlap_with(other)
        assert actual == expected
