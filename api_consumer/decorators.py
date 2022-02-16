import functools
from typing import Any, Type, Callable

from api_consumer.endpoints import Endpoint


def noop(value: Any) -> Any:
    return value


def endpoint(endpoint_class: Type[Endpoint]):
    def decorator(func):
        @functools.wraps(func)
        def decorated_func(self, *args, **kwargs):
            endpoint = endpoint_class(*args, **kwargs)
            response = self.call(endpoint)
            return endpoint.get_value(response)

        return decorated_func

    return decorator
