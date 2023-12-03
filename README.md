# API Consumer

Create clients for consuming endpoints in a class-based way.

## Installation
```shell
pip install api-client-framework
```


## Describe the endpoints using a class
```python
from api_client_framework.requests import RequestsEndpoint
from api_client_framework.requests import Methods
from api_client_framework.parsers import NamedTupleParser
from collections import namedtuple

User = namedtuple("User", ["id", "uid", "password","first_name", ...], rename=True)

class UsersEndpoint(RequestsEndpoint):
    method = Methods.GET
    url = "https://random-data-api.com/api/v2/users"
    params = {"response_type": "json"}
    parser = NamedTupleParser(User)
```

## Create your client
```python
import requests

from examples.random_data_api.endpoints import UsersEndpoint
from examples.random_data_api.models import User
from api_client_framework.requests import RequestsClient


class RandomDataAPI(RequestsClient):
    """Client for random-data-api.com"""

    def __init__(self):
        self.session = requests.Session()

    def get_user(self) -> User:
        """Retrieve a single random user"""
        return self._perform_request(UsersEndpoint())
```

## Advanced
### Create your own data parsers
...using `Parser` protocol.

### Convert HTTP exceptions in your custom exceptions
...by creating your own `exception_handler`

### Define a base URL for all your endpoints only once
...using `BaseUrlSession` from [requests_toolbelt](https://toolbelt.readthedocs.io/) package

### Log responses
...by adding [a hook](https://requests.readthedocs.io/en/latest/user/advanced/#event-hooks) in your `requests.Session` instance

```python
def print_response(response, *args, **kwargs):
    print(response.url)

session = requests.Session()
session.hooks.setdefault("response", [])
session.hooks["response"].append(print_response)
```


## Examples
There's a small example in this repo, under [`examples/random_data_api`](https://github.com/EnriqueSoria/api_client_framework/tree/master/examples/random_data_api), which implements some endpoints of [random-data-api.com](https://random-data-api.com/)

### Made with `api_client_framework`
 - [PyWegowAPI](https://github.com/EnriqueSoria/PyWegowAPI) -  A client for the public, undocumented, Wegow API 
