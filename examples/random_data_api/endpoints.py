from examples.random_data_api.models import Beer
from examples.random_data_api.models import User
from api_client_framework.methods import Methods
from api_client_framework.parsers import NamedTupleParser
from api_client_framework.requests import RequestsEndpoint


class UsersEndpoint(RequestsEndpoint):
    method = Methods.GET
    url = "https://random-data-api.com/api/v2/users"
    params = {"response_type": "json"}
    parser = NamedTupleParser(User)


class BeersEndpoint(RequestsEndpoint):
    method = Methods.GET
    url = "https://random-data-api.com/api/v2/beers"
    params = {"response_type": "json"}
    parser_class = NamedTupleParser
    models = {"response": Beer}
