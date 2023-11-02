import requests

from api_client_framework.requests import RequestsClient

from examples.random_post_api.endpoints import CreateObjectEndpoint
from examples.random_post_api.models import CreateObjectRequest


class ObjectsAPI(RequestsClient):
    """Client for https://restful-api.dev/"""

    def __init__(self):
        self.session = requests.Session()

    def create_object(self, data: CreateObjectRequest):
        return self._perform_request(CreateObjectEndpoint(data))
