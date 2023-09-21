from dataclasses import dataclass
from typing import Any


@dataclass
class Request:
    # TODO: need to clone Request & Response?
    method: str
    url: str
    headers: dict | None
    files: list


@dataclass
class Response:
    ...


@dataclass
class Page:
    number: int
    items_per_page: int
    item_count: int
