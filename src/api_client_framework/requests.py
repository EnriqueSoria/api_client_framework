from __future__ import annotations

from dataclasses import field
from json import JSONDecodeError
from typing import Any
from typing import Callable

import requests

from api_client_framework.methods import Methods
from api_client_framework.parsers import NoOpParser
from api_client_framework.protocols import EndpointProtocol
from api_client_framework.protocols import ExceptionHandler
from api_client_framework.protocols import Parser


class ExceptionReRaiser(ExceptionHandler):
    def __call__(self, exception: Exception, response: requests.Response):
        raise exception


class RequestsEndpoint(EndpointProtocol):
    method: str = Methods.GET
    url: str
    params: dict | None = None
    data: Any = None
    default_headers: dict | None = None

    models: dict[str, Parser] = field(default_factory=dict)
    exception_handler: Callable[[Exception], Any] = ExceptionReRaiser()

    def get_parser(self, model_name: str) -> Parser:
        try:
            return self.models[model_name]
        except KeyError:
            return NoOpParser(...)

    def get_url(self) -> str:
        return self.url

    def get_headers(self):
        return self.get_parser("headers").to_dict(self.default_headers)

    def get_params(self):
        return self.get_parser("params").to_dict(self.params)

    def get_data(self):
        return self.get_parser("request").to_dict(self.data)

    def get_request(self):
        return requests.Request(
            method=self.method,
            url=self.get_url(),
            params=self.get_params(),
            headers=self.get_headers(),
            json=self.get_data(),
        )

    def handle_exception(self, exception: Exception, response: requests.Response):
        return self.exception_handler(exception, response)

    def parse_response(self, response: requests.Response):
        try:
            data = response.json()
        except JSONDecodeError:
            return response.text

        return self.get_parser("response").to_class(data)

    def handle_response(self, response: requests.Response):
        try:
            response.raise_for_status()
        except requests.RequestException as exception:
            return self.exception_handler(exception, response)

        return self.parse_response(response)


class RequestsClient:
    session: requests.Session

    def _perform_request(self, endpoint: EndpointProtocol):
        request = endpoint.get_request()
        prepared_request = self.session.prepare_request(request)
        response = self.session.send(prepared_request)
        return endpoint.handle_response(response)
