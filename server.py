import os
import requests
from flask import Flask
import werkzeug
from werkzeug.wrappers import Response
from graphviz import Source

HOST = os.environ['HOST']

app = Flask(__name__)


def url(path):
    return "{}/{}".format(HOST, path)

def render(path, format="png"):
    dot_url = url(path)
    response = requests.get(dot_url)

    if response.status_code == 200:
        src = Source(response.text)
    else:
        raise IOError("Problem finding: {}".format(dot_url))

    return src.pipe(format=format)

@app.route("/")
def welcome():
    return "Welcome.  Configured to:{}".format(HOST)

@app.route("/<path:path>")
def render_url(path, format="png"):
    try:
        return Response(render(path, format), mimetype="image/{}".format(format))
    except IOError as err:
        return err.message, 400

