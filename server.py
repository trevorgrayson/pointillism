import os
from flask import Flask
import werkzeug
from werkzeug.wrappers import Response
from renderer import render

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
  

@app.route("/")
def welcome():
    return "Welcome.  Configured to:{}".format(HOST)

@app.route("/.<path:path>\.<regex(\"[a-zA-Z0-9]{3}\"):format>")
def render_url_with_format(path):
    if format == 'dot':
      render_url(".".join((path, "dot")))

def response(path, format):
    return Response(render(HOST, path, format), 
                    mimetype="image/{}".format(get_mime(format)))

@app.route("/<path:path>")
def render_url(path):
    format = path[len(path)-3:]
    path = path[:len(path)-4]

    try:
        return response(path, format)

    except IOError as err:
        return str(err), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=IS_DEV) 
