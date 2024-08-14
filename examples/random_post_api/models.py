from collections import namedtuple

CreateObjectResponse = namedtuple("Object", ["id", "name", "data", "createdAt"])

CreateObjectRequest = namedtuple("Object", ["name", "data"])
