from __future__ import annotations

from dataclasses import dataclass
from dataclasses import is_dataclass, asdict

from typing import Optional, Any, Mapping, Dict, Union, cast

import requests
from dacite import from_dict

from api_consumer import protocols
from api_consumer.httpverb import HttpVerb


class URLBuilder:
    def build(self, endpoint: Endpoint) -> str:  # TODO: Add more parameters
        return endpoint.url

    def get_query_params(self) -> Mapping:
        ...


class ResponseParser:
    """Parses response (convert to pydantic/dataclass...)"""

    def parse(self, response):
        ...


class Paginator:
    """Handles pagination"""

    def has_next_page(self) -> bool:
        ...

    def get_next_page(self, response) -> Page:
        ...

    def get_list(self, response) -> list:
        ...


class Endpoint(protocols.Endpoint):
    method: str = HttpVerb.GET
    url: str
    json: bool = True  # Whether to send body as file-like or json
    default_headers: Optional[dict] = {}

    result: Optional[Any]  # Dataclass to store the result

    # Dependencies
    url_builder = URLBuilder
    paginator = Paginator

    def __init__(
        self,
        params: Optional[Any] = None,
        data: Optional[Any] = None,
        headers: Optional[dict] = None,
    ):
        """ """
        self.data = self.force_dict(data)
        self.params = self.force_dict(params)
        self.headers = {**self.default_headers, **self.force_dict(headers)}

    def __str__(self):
        return f"{self.method} {self.url}"

    def __repr__(self):
        return f"{self.__class__.__name__}(method={self.method}, url={self.url}, params={self.params}, data={self.data})"

    def __iter__(self):
        response = self.call()
        paginator = self.get_paginator()

        # TODO: Check if is list
        yield from paginator.get_list(response)

        while paginator.has_next_page(response):
            response = paginator.get_next_page()
            yield from paginator.get_list(response)

    def get_paginator(self):
        return self.paginator()

    def get_url_builder(self):
        return self.url_builder()

    def build_url(self) -> str:
        return URLBuilder().build(self)

    @staticmethod
    def force_dict(data) -> dict:
        if data is None:
            return {}

        if isinstance(data, dict):
            return data

        if is_dataclass(data):
            return asdict(data)

        return data

    def get_request(self) -> requests.Request:
        body_param = "json" if self.json else "data"
        body = {body_param: self.data}
        return requests.Request(
            method=self.method,
            url=self.url,
            params=self.params,
            headers=self.headers,
            **body,
        )

    def get_value(self, value: Dict[str, Any]) -> Any:
        if self.result is None:
            return value

        dataclass_value = from_dict(data_class=self.result, data=value)
        cast(self.result, dataclass_value)  # only for type-hinting
        return dataclass_value

    @classmethod
    def as_method(cls):
        def method_function(
            self,
            params: Optional[Any] = None,
            data: Optional[Any] = None,
            headers: Optional[dict] = None,
        ):
            endpoint = cls(params=params, data=data, headers=headers)
            response = self.call(endpoint)
            return endpoint.get_value(response)

        return method_function
