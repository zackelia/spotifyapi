""" This module provides various helper functions """
import json
import requests


def get(url, headers):
    """ GET request from a URL """
    r = requests.get(url, headers=headers)
    r.raise_for_status()

    return r


def put(url, data, headers):
    """ PUT request to a URL with data """
    r = requests.put(url, data=json.dumps(data), headers=headers)
    r.raise_for_status()

    return r
