Let's take this endpoint as an example: [ttps://random-data-api.com/api/v2/beers](ttps://random-data-api.com/api/v2/beers)

It returns something like this:
```json
{
  "id": 1946,
  "uid": "2bfff819-80c4-4221-9151-cb3c32155e62",
  "brand": "Blue Moon",
  "name": "Chocolate St",
  "style": "Bock",
  "hop": "Warrior",
  "yeast": "3787 - Trappist High Gravity",
  "malts": "Vienna",
  "ibu": "95 IBU",
  "alcohol": "2.3%",
  "blg": "17.0°Blg"
}
```

We're going to create a `namedtuple` to hold the response values:
```python
from collections import namedtuple

field_names = [ "id", "uid", "brand", "name", "style", "hop", "yeast", "malts", "ibu", "alcohol", "blg", ]
Beer = namedtuple("Beer", field_names, rename=True)
```

Now that we've modelled how the response look, we have to describe the endpoint:
```python
from api_client_framework.requests import RequestsEndpoint
from api_client_framework.requests import Methods
from api_client_framework.parsers import NamedTupleParser

class BeersEndpoint(RequestsEndpoint):
    method = Methods.GET
    url = "https://random-data-api.com/api/v2/beers"
    params = {"response_type": "json"}
    parser = NamedTupleParser(Beer)
```