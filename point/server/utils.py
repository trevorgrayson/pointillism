from werkzeug.routing import BaseConverter
from werkzeug.wrappers import Response
from point.renderer import get_and_render, Forbidden
from config import HOST, STATIC_DIR

MIME_MAP = {
    'svg': 'svg+xml'
}


def get_mime(format):
    return MIME_MAP.get(format, format)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def headers(user=None, **config):
    heads = {

    }

    if user and user.git_token:
        heads['Authorization'] = f'token {user.git_token}'

    return heads


def response(path, format, host=HOST, **params):
    try:
        return Response(get_and_render(host, path, format, **params),
                        mimetype="image/{}".format(get_mime(format)))
    except IOError as err:
        with open(STATIC_DIR + '/images/pointillism-404.svg', 'r') as fp:
            return Response(fp.read(), status=404,
                            mimetype="image/svg+xml")
    except Forbidden as err:
        with open(STATIC_DIR + '/images/pointillism-401.svg', 'r') as fp:
            return Response(fp.read(), status=401,
                            mimetype="image/svg+xml")
