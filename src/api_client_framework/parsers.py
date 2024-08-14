from __future__ import annotations

from typing import Iterable
from typing import NamedTuple
from typing import Type
from typing import TypeVar

from api_client_framework.protocols import Parser

T = TypeVar("T")


class NoOpParser(Parser):
    def __init__(self, model, **kwargs): ...  # Dummy implementation to match with protocol

    def to_dict(self, instance: T) -> T:
        return instance

    def to_class(self, dictionary: T) -> T:
        return dictionary


Model = TypeVar("Model", bound=NamedTuple)


class NamedTupleParser(Parser):
    def __init__(self, model: Type[Model] | None, *, many: bool = False, **kwargs):
        self.model = model
        self.many = many

    def single_item_to_dict(self, instance: NamedTuple) -> dict:
        return instance._asdict()

    def multiple_items_to_dict(self, instance: Iterable[NamedTuple]) -> list[dict]:
        return [self.single_item_to_dict(item) for item in instance]

    def to_dict(self, instance: NamedTuple | Iterable[NamedTuple]) -> dict | list[dict]:
        if self.many:
            return self.multiple_items_to_dict(instance)

        return self.single_item_to_dict(instance)

    def single_item_to_class(self, instance: dict) -> Model:
        return self.model(**instance)

    def multiple_items_to_class(self, instance: list[dict]) -> list[Model]:
        return [self.single_item_to_class(item) for item in instance]

    def to_class(self, dictionary: dict) -> Model | list[Model]:
        if self.many:
            return self.multiple_items_to_class(dictionary)

        return self.single_item_to_class(dictionary)
