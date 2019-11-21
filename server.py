import os
from flask import Flask, request
import werkzeug
from werkzeug.wrappers import Response
from renderer import render
from urllib.parse import urlparse

HOST = os.environ['HOST']
ENV = os.environ.get('ENV', "PROD")

app = Flask(__name__)

## Extract out
from werkzeug.routing import BaseConverter
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

# Extract End

IS_DEV = (ENV == "develop")

MIME_MAP = {
  'svg': 'svg+xml'
}


def get_mime(format):
  return MIME_MAP.get(format, format)
  
def response(path, format, host=HOST):
    return Response(render(host, path, format), 
                    mimetype="image/{}".format(get_mime(format)))

@app.route("/")
def welcome():
    return "Welcome.  Configured to:{}".format(HOST)

@app.route("/rel/<path:path>")
def render_relative_path(path):
    """ Find the path on the referring host's server """
    format = path[len(path)-3:]
    path = path[:len(path)-4]
    referrer = request.referrer or None
    if referer is None:
        return "No referring URL.", 404

    host = urlparse(referrer).hostname

    if format in ["dot", "gv"]:
        path = ".".join((path, format))
        format = "png"

    try:
        return response(path, format, host=host)

    except IOError as err:
        return str(err), 400

@app.route("/crib/.<path:path>\.<regex(\"[a-zA-Z0-9]{3}\"):fileFormat>\.<regex(\"[a-zA-Z0-9]{3}\"):format>")
def render_crib_with_format(path):
    if format == 'dot': # no filename, use default
      render_url(".".join((path, fileFormat, "png")))

@app.route("/crib/<path:path>")
def render_crib(path):
    format = path[len(path)-3:]
    path = path[:len(path)-4]

    if format in ["dot", "gv"]:
        path = ".".join((path, format))
        format = "png"

    try:
        return response(path, format)

    except IOError as err:
        return str(err), 400

@app.route("/.<path:path>\.<regex(\"[a-zA-Z0-9]{3}\"):fileFormat>\.<regex(\"[a-zA-Z0-9]{3}\"):format>")
def render_url_with_format(path):
    if format == 'dot': # no filename, use default
      render_url(".".join((path, fileFormat, "png")))

@app.route("/<path:path>")
def render_url(path):
    format = path[len(path)-3:]
    path = path[:len(path)-4]

    if format in ["dot", "gv"]:
        path = ".".join((path, format))
        format = "png"

    try:
        return response(path, format)

    except IOError as err:
        return str(err), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=IS_DEV) # port doesn't work?
