from __future__ import annotations

from typing import NamedTuple
from typing import Type
from typing import TypeVar

from api_client_framework.protocols import Parser


class NoOpParser(Parser):
    def __init__(self, model, **kwargs): ...  # Dummy implementation to match with protocol

    def to_dict(self, instance: dict) -> dict:
        return instance

    def to_class(self, dictionary: dict) -> dict:
        return dictionary


Model = TypeVar("Model", bound=NamedTuple)


class NamedTupleParser(Parser):
    def __init__(self, model: Type[Model] | None, **kwargs):
        self.model = model

    def to_dict(self, instance: NamedTuple) -> dict:
        return instance._asdict()

    def to_class(self, dictionary: dict) -> Model | dict:
        return self.model(**dictionary)
