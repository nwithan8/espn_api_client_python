import requests


def get(url: str):
    return requests.get(url)


def get_json(url: str):
    return get(url=url).json()
