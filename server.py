import os
from flask import Flask
import werkzeug
from werkzeug.wrappers import Response
from renderer import render

HOST = os.environ['HOST']

app = Flask(__name__)

@app.route("/")
def welcome():
    return "Welcome.  Configured to:{}".format(HOST)

@app.route("/<path:path>")
def render_url(path, format="png"):
    try:
        return Response(render(HOST, path, format), 
                        mimetype="image/{}".format(format))

    except IOError as err:
        return err.message, 400

