from typing import Any
from typing import NamedTuple
from typing import Type

from api_client_framework.protocols import Parser


class NoOpParser(Parser):
    def to_dict(self, instance: dict) -> dict:
        return instance

    def to_class(self, dictionary: dict) -> dict:
        return dictionary


class NamedTupleParser(Parser):
    def __init__(self, named_tuple_class: Type[NamedTuple]):
        self.named_tuple_class = named_tuple_class

    def to_dict(self, instance: NamedTuple) -> dict:
        try:
            return instance._asdict()
        except AttributeError:
            return instance

    def to_class(self, dictionary: dict) -> Any:
        return self.named_tuple_class(**dictionary)
