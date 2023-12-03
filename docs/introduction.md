# API Client Framework

Create clients for consuming endpoints in a class-based way.

 - Describe endpoints as classes
 - Let your users send and receive data using python classes, not dicts.
 - Embrace good practices

```pycon
>>> from examples.random_data_api.client import RandomDataAPI
>>> client = RandomDataAPI()
>>> beer = client.get_beer()
>>> print(f"{beer.name} ({beer.style})")
Samuel Smith’s Oatmeal Stout (Wood-aged Beer)
```


## Installation
```shell
pip install api-client-framework
```

## Examples
There's a small example in this repo, under [`examples/random_data_api`](https://github.com/EnriqueSoria/api_client_framework/tree/master/examples/random_data_api), which implements some endpoints of [random-data-api.com](https://random-data-api.com/)

### Made with `api_client_framework`
 - [PyWegowAPI](https://github.com/EnriqueSoria/PyWegowAPI) -  A client for the public, undocumented, Wegow API 
