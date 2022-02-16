def ensure_ending_slash(url: str) -> str:
    ending = "/" if not url.endswith("/") else ""
    return url + ending
