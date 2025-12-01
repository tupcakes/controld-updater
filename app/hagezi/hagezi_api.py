import requests


def get_domains(url):
    with requests.get(url) as response:
        response.raise_for_status()
        json_data = response.json()
    return [rule["PK"] for rule in json_data.get("rules", [])]


def get_do(url):
    with requests.get(url) as response:
        response.raise_for_status()
        json_data = response.json()
    return json_data["group"]["action"]["do"]
