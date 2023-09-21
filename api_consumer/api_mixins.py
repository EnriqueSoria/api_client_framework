import json
from json import JSONDecodeError
from typing import Any
from typing import Optional

import requests
import structlog
from requests import Response

from api_consumer.endpoints import Endpoint
from api_consumer.requests_utils import parse_response

logger = structlog.get_logger(__name__)


class ExceptionConverter:
    def __call__(self, exception, endpoint, response):  # TODO: Rethink API
        return exception


class LogHandler:
    def exception(self, endpoint, response, exception):
        self.log_exception(
            endpoint=endpoint,
            response=response,
            exception=exception,
        )


class ExceptionHandler:
    raise_exceptions: bool
    exception_converter: Any

    def __call__(self, endpoint, response, exception):
        # Convert exception in custom exception
        original_exception = exception

        exception_converter = self.exception_converter()
        exception = exception_converter(exception)

        # Log only non-converted exceptions
        if exception is original_exception:
            self.log_exception(
                endpoint=endpoint,
                response=response,
                exception=exception,
            )

        # Raise exceptions if desired
        if self.raise_exceptions:
            raise exception


class ResponseParser:
    """Parse responses (i.e.: convert to dataclasses or pydantic models)"""


class ResponseHandler:
    ...


class ResponseHandlingMixin:
    @staticmethod
    def get_response_json_or_text(response, dump_dict=False):
        if response is None:
            return ""

        try:
            content = response.json()
            content = json.dumps(content, indent=2) if dump_dict else content
        except JSONDecodeError:
            content = response.text
        return content

    @staticmethod
    def build_logging_messsage(
        endpoint: Optional[Endpoint],
        response: Optional[Response],
    ) -> dict:
        if response is None:
            return {
                "endpoint": str(endpoint),
                "request": endpoint.data if isinstance(endpoint, Endpoint) else None,
            }

        content = ResponseHandlingMixin.get_response_json_or_text(response)
        endpoint_name = str(endpoint) if endpoint else response.url
        return {
            "endpoint": endpoint_name,
            "response": content,
            "request": (
                endpoint.data
                if isinstance(endpoint, Endpoint)
                else response.request.body
            ),
            "response_code": response.status_code,
        }

    @staticmethod
    def get_endpoint_name(endpoint, response) -> str:
        if endpoint:
            return str(endpoint)

        return f"{response.request.method} {response.url}"

    def log_exception(self, endpoint, response, exception):
        logger.exception(
            exception,
            extra=ResponseHandlingMixin.build_logging_messsage(endpoint, response),
        )

    def convert_exception(self, exc) -> Exception:
        """Method to allow converting exception into custom ones"""
        return exc

    def handle_exception(self, endpoint, response, exception, raise_exceptions: bool):
        # Convert exception in custom exception
        original_exception = exception
        exception = self.convert_exception(exception)

        # Log only non-converted exceptions
        if exception is original_exception:
            self.log_exception(
                endpoint=endpoint,
                response=response,
                exception=exception,
            )

        # Raise exceptions if desired
        if raise_exceptions:
            raise exception

    def handle_response(
        self,
        response: requests.Response,
        endpoint: Optional[Endpoint],
        raise_exceptions: bool = False,
    ) -> Optional[dict]:
        try:
            # Raise errors
            response.raise_for_status()
        except requests.HTTPError as exception:
            self.handle_exception(endpoint, response, exception, raise_exceptions)
        else:
            # Log endpoint info
            endpoint_name = ResponseHandlingMixin.get_endpoint_name(endpoint, response)
            logger.info(
                f"Calling {endpoint_name}",
                **ResponseHandlingMixin.build_logging_messsage(endpoint, response),
            )
            return parse_response(response)
