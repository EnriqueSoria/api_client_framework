from __future__ import annotations

import requests

from examples.random_data_api.endpoints import BeerDetailEndpoint
from examples.random_data_api.endpoints import BeerListEndpoint
from examples.random_data_api.endpoints import UsersEndpoint
from examples.random_data_api.models import Beer
from examples.random_data_api.models import User
from api_client_framework.requests import RequestsClient


class RandomDataAPI(RequestsClient):
    """Client for random-data-api.com"""

    def __init__(self):
        self.session = requests.Session()

    def get_user(self) -> User:
        """Retrieve a single random user"""
        return self._perform_request(UsersEndpoint())

    def get_users(self, count: int) -> list:
        """Retrieve a list of random users"""
        endpoint = UsersEndpoint()
        endpoint.params["size"] = count
        return self._perform_request(endpoint)

    def get_beer(self) -> Beer:
        """Retrieve a single random beer"""
        return self._perform_request(BeerDetailEndpoint())

    def get_beers(self, size: int = 10) -> list[Beer]:
        """Retrieve a list of random beers"""
        return self._perform_request(BeerListEndpoint(size=size))
