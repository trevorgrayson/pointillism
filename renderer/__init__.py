import os
import logging
import requests
from graphviz import Source

logging.basicConfig(filename='pointillism.log',level=logging.DEBUG)
LOG = logging.getLogger(__name__)

class NotFound(Exception): pass
class Forbidden(Exception): pass

def url(host, path, **params):
    ps = "&".join([f"{k}={v}" for k, v in params.items()])
    return "{}/{}?{}".format(host, path, ps) 


# look up this dict method
def render(host, path, format="png", headers={}, **params):
    dot_url = url(host, path, **params)
    LOG.debug(f"GET: {dot_url}")
    response = requests.get(dot_url, headers=headers)

    if response.status_code == 200:
        src = Source(response.text)
        return src.pipe(format=format)
    elif response.status_code == 401:
        raise Forbidden('Forbidden! http://pointillism.io/github/login')
    else:
        raise IOError("Problem finding: {}".format(dot_url))

