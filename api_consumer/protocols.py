from typing import Any
from typing import Protocol
from typing import TypeVar

from api_consumer.models import Page


class ConnectionHandler:
    def perform_request(self, endpoint):
        ...


class Endpoint(Protocol):
    def get_request(self) -> Any:
        ...

    def handle_response(self, response: Any) -> Any:
        ...


class DictToClass(Protocol):
    def to_dict(self, instance: Any) -> dict:
        ...

    def to_class(self, data_class: Any, dictionary: dict) -> Any:
        ...


class Paginator(Protocol):
    """Handles pagination"""

    def has_next_page(self) -> bool:
        ...

    def get_next_page(self, response) -> Page:
        ...

    def get_list(self, response) -> list:
        ...
