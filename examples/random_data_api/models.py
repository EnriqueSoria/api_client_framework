from collections import namedtuple

User = namedtuple(
    "User",
    [
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
    ],
    rename=True,
)

Beer = namedtuple(
    "Beer",
    [
        "id",
        "uid",
        "brand",
        "name",
        "style",
        "hop",
        "yeast",
        "malts",
        "ibu",
        "alcohol",
        "blg",
    ],
    rename=True,
)
