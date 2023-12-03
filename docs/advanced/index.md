### Create your own data parsers
...using `Parser` protocol.

### Convert HTTP exceptions in your custom exceptions
...by creating your own `exception_handler`

### Define a base URL for all your endpoints only once
...using `BaseUrlSession` from [requests_toolbelt](https://toolbelt.readthedocs.io/) package

### Log responses
...by adding [a hook](https://requests.readthedocs.io/en/latest/user/advanced/#event-hooks) in your `requests.Session` instance

```python
import requests

def print_response(response, *args, **kwargs):
    print(response.url)

session = requests.Session()
session.hooks.setdefault("response", [])
session.hooks["response"].append(print_response)
```
