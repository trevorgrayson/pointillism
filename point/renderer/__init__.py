import logging
import requests
from graphviz import Source
from point.theme import theme_inject, THEME

logging.basicConfig(filename='pointillism.log', level=logging.DEBUG)
LOG = logging.getLogger(__name__)


class NotFound(Exception):
    pass


class Forbidden(Exception):
    pass


def url(host, path, **params):
    ps = "&".join([f"{k}={v}" for k, v in params.items()])
    return "{}/{}?{}".format(host, path, ps) 


# look up this dict method
def render(host, path, format="png", theme=None, headers={}, **params):
    dot_url = url(host, path, **params)
    LOG.debug(f"GET: {dot_url}")
    LOG.debug(f'headers: {headers}')
    response = requests.get(dot_url, headers=headers)

    if response.status_code == 200:
        body = response.text
        body = theme_inject(body, theme)
        src = Source(body)
        return src.pipe(format=format)
    elif response.status_code == 401:
        raise Forbidden('Forbidden! http://pointillism.io/github/login')
    else:
        raise IOError("Problem finding: {}".format(dot_url))

