from dataclasses import asdict
from dataclasses import dataclass
from typing import Optional, Type, Any

import dacite
import requests
import structlog
from requests import Request, PreparedRequest
from requests_toolbelt.sessions import BaseUrlSession

from api_consumer import protocols
from api_consumer.api_mixins import ResponseHandlingMixin
from api_consumer.endpoints import Endpoint
from api_consumer.httpverb import HttpVerb

from api_consumer.models import Response
from api_consumer.protocols import ConnectionHandler

logger = structlog.get_logger(__name__)


class CustomBaseUrlSession(BaseUrlSession):
    def prepare_request(self, request: Request) -> PreparedRequest:
        request.url = self.create_url(url=request.url)
        return super().prepare_request(request)


class RequestsConnectionHandler(protocols.ConnectionHandler):
    """A concrete implementation of ConnectionHandler using the library `requests`"""

    def __init__(self, session: requests.Session):
        self.session = session

    def perform_request(self, endpoint) -> requests.Response:
        request = endpoint.get_request()
        prepared_request = self.session.prepare_request(request)
        response = self.session.send(prepared_request)
        return endpoint.handle_response(response)


class APIConsumer(ResponseHandlingMixin):
    default_base_url: Optional[str] = None
    timeout_in_seconds: Optional[float] = None

    def __init__(self, connection_handler: protocols.ConnectionHandler):
        self.connection_handler = connection_handler

    def _perform_request(self, endpoint: protocols.Endpoint, **kwargs):
        # TODO: Does endpoint need some args?
        return self.connection_handler.perform_request(endpoint)


class DaciteParser(protocols.DictToClass):
    def to_dict(self, instance: Any) -> dict:
        return asdict(instance)

    def to_class(self, data_class: Type, dictionary: dict) -> Any:
        return dacite.from_dict(data_class, dictionary)


class RequestsEndpoint(protocols.Endpoint):
    method: HttpVerb | str
    url: str

    default_headers: dict | None = None
    params: dict | None

    class_converter: protocols.DictToClass

    def __init__(self, params: dict | None = None, extra_headers: dict | None = None):
        self.extra_headers = extra_headers

    def get_method(self) -> str:
        return HttpVerb(self.method).value

    def get_url(self) -> str:
        return self.url

    def get_headers(self) -> dict | None:
        if self.default_headers is None and self.extra_headers is None:
            return None

        headers = {}
        headers.update(self.default_headers or {})
        headers.update(self.extra_headers or {})
        return headers

    def get_params(self) -> dict | None:
        return self.params

    def get_request(self) -> Request:
        return requests.Request(
            method=self.get_method(),
            url=self.url,
            headers=self.get_headers(),
            params=self.params,
            data=self.data,
        )


def merge_dicts(a: dict | None, b: dict | None) -> dict | None:
    if a is None and b is None:
        return None

    headers = {}
    headers.update(a or {})
    headers.update(b or {})
    return headers


class ReqEndpoint(requests.Request):
    method: HttpVerb | str
    url: str
    default_headers: dict | None = None

    def __init__(
        self,
        extra_headers: dict | None = None,
        files=None,
        data=None,
        params=None,
        auth=None,
        cookies=None,
        hooks=None,
        json=None,
    ):
        super().__init__(
            method=self.method,
            url=self.url,
            headers=merge_dicts(self.default_headers, extra_headers),
            files=files,
            data=data,
            params=params,
            auth=auth,
            cookies=cookies,
            hooks=hooks,
            json=json,
        )


class ClassBasedRequestsEndpoint(Endpoint):
    params_spec: Type | None = None
    data_spec: Type | None = None
    response_spec: Type | None = None

    class_converter: protocols.DictToClass

    def _force_dict(self, data: Any, spec: Type | None) -> dict:
        if spec is not None and isinstance(data, spec):
            return self.class_converter.to_dict(data)

        return data

    def __init__(
        self,
        extra_headers: dict | None = None,
        data=None,
        params=None,
    ):
        super().__init__(
            data=self._force_dict(data, self.data_spec),
            params=self._force_dict(params, self.params_spec),
            headers=merge_dicts(self.default_headers, extra_headers),
        )

    def handle_response(self, response: Any) -> Any:
        data = super().handle_response(response)
        return self._force_dict(data, self.response_spec)


@dataclass
class Params:
    query: str
    page: int = 1
    page_size: int = 20
    region: str = "es-es"
    mongo: bool = True


class SearchEndpoint(ClassBasedRequestsEndpoint):
    method = HttpVerb.GET
    url = "/api/search/events/"
    params_spec = Params
    response_spec = None

    class_converter = DaciteParser()


class PaginatedResponseMixin:
    def has_next_page(self) -> bool:
        return bool(self.next_page)

    def __len__(self):
        return self.events_count


class Consumer:
    def __init__(self, connection_handler):
        ...


class WegowAPI(APIConsumer):
    base_url = "https://www.wegow.com"

    def __init__(self):
        connection_handler = RequestsConnectionHandler(
            session=CustomBaseUrlSession(base_url=self.base_url)
        )
        super().__init__(connection_handler=connection_handler)

    def search_event(self, term: str):
        endpoint = SearchEndpoint(params=SearchEndpoint.params_spec(term))
        return self.connection_handler.perform_request(endpoint)


if __name__ == "__main__":
    api_consumer = WegowAPI()
    print(api_consumer.search_event("festival"))
