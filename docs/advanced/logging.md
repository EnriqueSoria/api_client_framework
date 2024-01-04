

### Log responses
...by adding [a hook](https://requests.readthedocs.io/en/latest/user/advanced.html#event-hooks) in your `requests.Session` instance

```python
import requests

def print_response(response, *args, **kwargs):
    print(response.url)

session = requests.Session()
session.hooks.setdefault("response", [])
session.hooks["response"].append(print_response)
```