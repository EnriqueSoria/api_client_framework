from typing import Any
from typing import Protocol


class EndpointProtocol(Protocol):
    def get_request(self) -> Any:
        ...

    def handle_exception(self, exception: Exception) -> Any:
        ...

    def parse_response(self, response: Any) -> Any:
        ...

    def handle_response(self, response: Any) -> Any:
        ...


class Parser(Protocol):
    def to_dict(self, instance: Any) -> dict:
        ...

    def to_class(self, dictionary: dict) -> Any:
        ...
