from typing import Optional, Type, Any

import requests
import structlog
from requests import Request, PreparedRequest
from requests_toolbelt.sessions import BaseUrlSession

from api_consumer.api_mixins import ResponseHandlingMixin
from api_consumer.endpoints import Endpoint

logger = structlog.get_logger(__name__)


class CustomBaseUrlSession(BaseUrlSession):
    def prepare_request(self, request: Request) -> PreparedRequest:
        request.url = self.create_url(url=request.url)
        return super().prepare_request(request)


def auto_func_maker(endpoint_class: Type[Endpoint], response_hint=Any):
    def method_function(
        self,
        params: Optional[Any] = None,
        data: Optional[Any] = None,
        headers: Optional[dict] = None,
    ) -> response_hint:
        endpoint = endpoint_class(params=params, data=data, headers=headers)
        response = self.call(endpoint)
        return endpoint.get_value(response)

    return method_function


class APIConsumer(ResponseHandlingMixin):
    default_base_url: Optional[str] = None
    timeout_in_seconds: Optional[float] = None

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or self.default_base_url
        self.session = self._get_session()

    def _get_session(self):
        return CustomBaseUrlSession(base_url=self.base_url)

    def perform_request(self, endpoint: Endpoint, **kwargs) -> requests.Response:
        request = endpoint.get_request()
        prepared_request = self.session.prepare_request(request)
        return self.session.send(prepared_request)

    def call(self, endpoint: Endpoint, raise_exceptions: bool = False, **kwargs):
        response = self.perform_request(endpoint, **kwargs)

        return self.handle_response(
            response, endpoint, raise_exceptions=raise_exceptions
        )
