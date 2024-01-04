from __future__ import annotations

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

    parser: Parser = NoOpParser()
    exception_handler: Callable[[Exception], Any] = ExceptionReRaiser()

    def get_url(self) -> str:
        return self.url

    def get_headers(self) -> dict | None:
        return self.default_headers

    def get_request(self):
        return requests.Request(
            method=self.method,
            url=self.get_url(),
            params=self.parser.to_dict(self.params),
            headers=self.parser.to_dict(self.get_headers()),
            json=self.parser.to_dict(self.data),
        )

    def handle_exception(self, exception: Exception, response: requests.Response):
        return self.exception_handler(exception, response)

    def parse_response(self, response: requests.Response) -> Any:
        try:
            data = response.json()
        except JSONDecodeError:
            return response.text

        return self.parser.to_class(data)

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
