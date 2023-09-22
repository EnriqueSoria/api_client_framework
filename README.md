# API Consumer

Create clients for consuming endpoints in a class-based way.


## Describe the endpoints using a class
```python
from api_consumer.requests import RequestsEndpoint
from api_consumer.requests import Methods
from api_consumer.parsers import NamedTupleParser
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
from src.api_consumer.requests import RequestsClient


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
...by adding a hook in your `requests.Session` instance