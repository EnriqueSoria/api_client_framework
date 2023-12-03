Let's take this endpoint as an example: [https://random-data-api.com/api/v2/users](https://random-data-api.com/api/v2/users)

It returns something like this:
```json
{
  "id": 9566,
  "uid": "a4bff8cb-1a39-421c-a297-b651271f4eab",
  "password": "w8ASr3zWM5",
  "first_name": "Erick",
  "last_name": "Beier",
  "username": "erick.beier",
  "email": "erick.beier@email.com",
  "avatar": "https://robohash.org/facerequoderror.png?size=300x300&set=set1",
  "gender": "Agender",
  "phone_number": "+599 1-662-572-1371",
  "social_insurance_number": "692093644",
  "date_of_birth": "1985-03-30",
  "employment": {
    "title": "Central Construction Orchestrator",
    "key_skill": "Teamwork"
  },
  "address": {
    "city": "North Dedratown",
    "street_name": "Christian Mountain",
    "street_address": "74531 Bruen Squares",
    "zip_code": "61875-9264",
    "state": "Wisconsin",
    "country": "United States",
    "coordinates": {
      "lat": -58.55381121679781,
      "lng": -16.770597141257525
    }
  },
  "credit_card": {
    "cc_number": "4429442440381"
  },
  "subscription": {
    "plan": "Business",
    "status": "Idle",
    "payment_method": "Credit card",
    "term": "Payment in advance"
  }
}
```

We're going to create a `namedtuple` to hold the response values:
```python
from collections import namedtuple

field_names = [
    "id",
    "uid",
    "password",
    "first_name",
    "last_name",
    "username",
    "email",
    "avatar",
    "gender",
    "phone_number",
    "social_insurance_number",
    "date_of_birth",
    "employment",
    "address",
    "credit_card",
    "subscription",
]
User = namedtuple("User", field_names, rename=True)
```

Now that we've modelled how the response look, we have to describe the endpoint:
```python
from api_client_framework.requests import RequestsEndpoint
from api_client_framework.requests import Methods
from api_client_framework.parsers import NamedTupleParser

class UsersEndpoint(RequestsEndpoint):
    method = Methods.GET
    url = "https://random-data-api.com/api/v2/users"
    params = {"response_type": "json"}
    parser = NamedTupleParser(User)
```