from os import path as p
import logging
from werkzeug.wrappers import Response
from point.renderer import get_and_render, Forbidden, get_mime
from config import HOST, STATIC_DIR

DOT_FORMATS = [".dot", ".gv", ""]


def headers(user=None, **_config):
    heads = {}
    if user and user.git_token:
        heads['Authorization'] = f'token {user.git_token}'

    return heads


def response(path, format, host=HOST, **params):
    try:
        return Response(get_and_render(host, path, format, **params),
                        mimetype="image/{}".format(get_mime(format)))
    except IOError as err:
        logging.exception(err)
        with open(STATIC_DIR + '/images/pointillism-404.svg', 'r') as fp:
            return Response(fp.read(), status=404,
                            mimetype="image/svg+xml")
    except Forbidden as err:
        logging.exception(err)
        with open(STATIC_DIR + '/images/pointillism-401.svg', 'r') as fp:
            return Response(fp.read(), status=401,
                            mimetype="image/svg+xml")


def parse_request_fmt(path):
    path, ext = p.splitext(path)

    if ext in DOT_FORMATS:
        return '.svg'

    return ext


def parse_request_path(path):
    truncated, ext = p.splitext(path)

    if ext in DOT_FORMATS:
        return path
    else:
        return truncated


def convert(org, project, path, creds=None,
            protocol="https", domain="pointillism.io"):
    """convert url parts into pointillism link"""
    url = "/".join((
        f"{protocol}://{domain}", org, project, path
    ))
    if creds:
        url += f"?token={creds}"

    return url
