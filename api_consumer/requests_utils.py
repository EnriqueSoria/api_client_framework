import json
from typing import Any

import requests


def parse_response(
    response: requests.Response, dump_dict: bool = False, default: Any = None
) -> Any:
    if response is None:
        return default

    try:
        content = response.json()
        content = json.dumps(content, indent=2) if dump_dict else content
    except json.JSONDecodeError:
        content = response.text
    return content
