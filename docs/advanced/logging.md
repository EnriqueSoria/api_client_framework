

### Log responses
...by adding [a hook](https://requests.readthedocs.io/en/latest/user/advanced.html#event-hooks) in your `requests.Session` instance

```python
import requests

from api_client_framework.requests import RequestsClient


def print_response(response, *args, **kwargs):
    print(response.url)


class YourAPIClient(RequestsClient):

    def __init__(self):
        # Initialise requests client as usual
        self.session = requests.Session()
        # Ensure hooks["response"] already exists
        self.session.hooks.setdefault("response", [])
        # Add print response hook
        self.session.hooks["response"].append(print_response)
```