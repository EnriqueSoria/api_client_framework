from dataclasses import is_dataclass, asdict

from typing import Optional, Any, Mapping, Dict, Union, cast

import requests
from dacite import from_dict

from api_consumer.methods import Methods


class Endpoint:
    method: str = Methods.GET
    url: str
    json: bool = True  # Whether to send body as file-like or json
    default_headers: Optional[dict] = {}

    result: Optional[Any]  # Dataclass to store the result

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
        self.url = self.build_url()

    def __str__(self):
        return f"{self.method} {self.url}"

    def __repr__(self):
        return f"{self.__class__.__name__}(method={self.method}, url={self.url}, params={self.params}, data={self.data})"

    def build_url(self) -> str:
        return self.url

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
