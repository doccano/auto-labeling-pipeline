from pydantic import BaseModel


class ClassificationLabel(BaseModel):
    label: str


class SequenceLabel(BaseModel):
    label: str
    start_offset: int
    end_offset: int


class Seq2seqLabel(BaseModel):
    text: str
