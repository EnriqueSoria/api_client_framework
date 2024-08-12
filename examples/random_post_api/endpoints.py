from api_client_framework.methods import Methods
from api_client_framework.parsers import NamedTupleParser
from api_client_framework.requests import RequestsEndpoint

from examples.random_post_api.models import CreateObjectRequest, CreateObjectResponse


class CreateObjectEndpoint(RequestsEndpoint):
    method = Methods.POST
    url = "https://api.restful-api.dev/objects/"
    default_headers = {"content-type": "application/json"}
    parser_class = NamedTupleParser
    models = {
        "request": CreateObjectRequest,
        "response": CreateObjectResponse,
    }

    def __init__(self, data: CreateObjectRequest):
        self.data = data
