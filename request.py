import requests


def get(url):
    return requests.get(url)


def _json(url):
    return get(url).json()
