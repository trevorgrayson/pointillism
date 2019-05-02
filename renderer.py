import os
import requests
from graphviz import Source

def url(host, path):
    return "{}/{}".format(host, path)

def render(host, path, format="png"):
    dot_url = url(host, path)
    response = requests.get(dot_url)

    if response.status_code == 200:
        src = Source(response.text)
    else:
        raise IOError("Problem finding: {}".format(dot_url))

    return src.pipe(format=format)
