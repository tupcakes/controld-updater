import requests


def api_request(method, url, headers, payload=None):
    """Generic API request handler."""
    response = requests.request(method, url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()
