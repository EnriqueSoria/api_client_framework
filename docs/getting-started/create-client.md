Finally, we're going to create a client class, which will be responsible for handling connections 
and providing a nice python interface for anyone that wants to use the API.

```python
import requests

from examples.random_data_api.endpoints import BeersEndpoint
from examples.random_data_api.models import Beer
from api_client_framework.requests import RequestsClient


class RandomDataAPI(RequestsClient):
    """Client for random-data-api.com"""

    def __init__(self):
        self.session = requests.Session()

    def get_beer(self) -> Beer:
        """Retrieve a single random beer"""
        return self._perform_request(BeersEndpoint())
```