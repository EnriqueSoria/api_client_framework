# Describe endpoints

##  Retrieving a random beer

Let's take this endpoint as an example: [ttps://random-data-api.com/api/v2/beers](ttps://random-data-api.com/api/v2/beers)

It returns something like this:

```json linenums="1"
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

```python linenums="1"
from collections import namedtuple

field_names = ["id", "uid", "brand", "name", "style", "hop", "yeast", "malts", "ibu", "alcohol", "blg"]
Beer = namedtuple("Beer", field_names, rename=True)
```

Now that we've modelled how the response look, we have to describe the endpoint:

```python linenums="1"
from api_client_framework.requests import RequestsEndpoint
from api_client_framework.requests import Methods
from api_client_framework.parsers import NamedTupleParser
from examples.random_data_api.models import Beer


class BeerDetailEndpoint(RequestsEndpoint):
    method = Methods.GET
    url = "https://random-data-api.com/api/v2/beers"
    params = {"response_type": "json"}
    parser_class = NamedTupleParser
    models = {"response": NamedTupleParser(Beer)}
```

## Retrieving a list of beers
To receive a list of beers instead, we can use the same endpoint, but passing a query param indicating how many beers 
we want to receive (i.e. `size=10`). 

We also need to tell our parser that we're going to receive `many` objects instead of one.

```python linenums="1" hl_lines="11 13-14"
from api_client_framework.requests import RequestsEndpoint
from api_client_framework.requests import Methods
from api_client_framework.parsers import NamedTupleParser
from examples.random_data_api.models import Beer


class BeerListEndpoint(RequestsEndpoint):
    method = Methods.GET
    url = "https://random-data-api.com/api/v2/beers"
    params = {"response_type": "json"}
    models = {"response": NamedTupleParser(model=Beer, many=True)}

    def __init__(self, size: int):
        self.params["size"] = size
```

