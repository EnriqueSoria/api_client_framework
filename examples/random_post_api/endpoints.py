import requests

from api_consumer.methods import Methods
from api_consumer.parsers import NamedTupleParser
from api_consumer.requests import RequestsEndpoint

from examples.random_post_api.models import CreateObjectRequest

class CreateObjectEndpoint(RequestsEndpoint):
    method = Methods.POST
    url = "https://api.restful-api.dev/objects/"
    default_headers = {"content-type": "application/json"}
    parser = NamedTupleParser(CreateObjectRequest)

    def __init__(self, data: CreateObjectRequest):
        self.data = data

    def get_request(self):
        return requests.Request(
            method=self.method,
            url=self.get_url(),
            params=self.parser.to_dict(self.params),
            headers=self.parser.to_dict(self.get_headers()),
            # need to send json data in "json" kwarg for
            # requests library to serialize the dict to json
            json=self.parser.to_dict(self.data),
        )
        return request