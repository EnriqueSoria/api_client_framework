from examples.random_data_api.models import Beer
from examples.random_data_api.models import User
from api_client_framework.methods import Methods
from api_client_framework.parsers import NamedTupleParser
from api_client_framework.requests import RequestsEndpoint


class UsersEndpoint(RequestsEndpoint):
    method = Methods.GET
    url = "https://random-data-api.com/api/v2/users"
    params = {"response_type": "json"}
    models = {"response": NamedTupleParser(User)}


class BeerListEndpoint(RequestsEndpoint):
    method = Methods.GET
    url = "https://random-data-api.com/api/v2/beers"
    params = {"response_type": "json"}
    models = {"response": NamedTupleParser(model=Beer, many=True)}

    def __init__(self, size):
        self.params["size"] = size


class BeerDetailEndpoint(RequestsEndpoint):
    method = Methods.GET
    url = "https://random-data-api.com/api/v2/beers"
    params = {"response_type": "json"}
    parser_class = NamedTupleParser
    models = {"response": NamedTupleParser(Beer)}
