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
def render_url(path):
    format = path[len(path)-3:]
    r_format = format

    if format == "svg":
        r_format = "svg+xml"

    path = path[:len(path)-4]

    try:
        return Response(render(HOST, path, format), 
                        mimetype="image/{}".format(r_format))

    except IOError as err:
        return str(err), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0")
