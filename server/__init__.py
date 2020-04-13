import logging
from flask import Flask, request, g, session
from string import Template
import werkzeug
from werkzeug.wrappers import Response
from renderer import render, Forbidden
from urllib.parse import urlparse
from config import DOMAIN, HOST, ENV, STATIC_DIR, PAYPAL_CLIENT_ID
from server.github import github_routes
from server.repos import repo_routes
from models.base import GitHubRepo

from config import ADMIN_USER, ADMIN_PASS, LDAP_BASE_DN, SECRET_KEY
from ldapauth.flask.routes import auth_routes, register_config
from flask_simpleldap import LDAP
from server.base import get_me

LOG = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(github_routes, url_prefix='/github')
app.register_blueprint(auth_routes)
app.register_blueprint(repo_routes)

register_config(app,
  ldap_host='localhost',
  ldap_base_dn=LDAP_BASE_DN,
  ldap_username=ADMIN_USER,
  ldap_password=ADMIN_PASS,
  ldap_login_view='auth.login'
)
app.config['SECRET_KEY'] = SECRET_KEY 
ldap = LDAP()

@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        # This is where you'd query your database to get the user info.
        g.user = {}
        # Create a global with the LDAP groups the user is a member of.
        # g.ldap_groups = ldap.get_user_groups(user=session['username'])


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
  

def get_params(request):
    params = {}

    params['token'] = request.cookies.get('github_token')

    if 'token' in request.args:
        params['token'] = request.args['token']

    return params


def response(path, format, host=HOST, **params):
    try:
        return Response(render(host, path, format, **params), 
                        mimetype="image/{}".format(get_mime(format)))
    except IOError as err:
        with open(STATIC_DIR + '/images/pointillism-404.svg', 'r') as fp:
            return Response(fp.read(), status=404,
                            mimetype="image/svg+xml")
    except Forbidden as err:
        with open(STATIC_DIR + '/images/pointillism-401.svg', 'r') as fp:
            return Response(fp.read(), status=401,
                            mimetype="image/svg+xml")


@app.route("/")
def welcome():
    with open(STATIC_DIR + '/index.html', 'r') as fp:
        template = Template(fp.read())

        return template.substitute(
            host=HOST,
            domain=DOMAIN,
            paypal_id=PAYPAL_CLIENT_ID
        )


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
        return response(path, format, host=host, **get_params(request))

    except IOError as err:
        return str(err), 400

@app.route("/crib/.<path:path>\.<regex(\"[a-zA-Z0-9]{3}\"):fileFormat>\.<regex(\"[a-zA-Z0-9]{3}\"):format>")
def render_crib_with_format(path):
    if format == 'dot': # no filename, use default
      render_crib(".".join((path, fileFormat, "png")))

@app.route("/crib/<path:path>")
def render_crib(path):
    format = path[len(path)-3:]
    path = path[:len(path)-4]

    if format in ["dot", "gv"]:
        path = ".".join((path, format))
        format = "png"

    try:
        return response(path, format, host="https://cribnot.es")

    except IOError as err:
        return str(err), 400

@app.route("/.<path:path>\.<regex(\"[a-zA-Z0-9]{3}\"):fileFormat>\.<regex(\"[a-zA-Z0-9]{3}\"):format>")
def render_url_with_format(path):
    if format == 'dot': # no filename, use default
      render_url(".".join((path, fileFormat, "png")))

@app.route("/github/<path:path>")
def render_github_url(path):
    # BUG: don't want to require owner to load first. or do you?
    user = get_me() 

    if user is not None:
        org, project, *_tail = path.split('/')
        repo = GitHubRepo.search_repo(user.name, org, project)

        if repo:
        raise Exception(str(repo))
    # TODO if repo in db, use creds
    format = path[len(path)-3:]
    path = path[:len(path)-4]

    if format in ["dot", "gv"]:
        path = ".".join((path, format))
        format = "png"

    try:
        return response(path, format, **get_params(request))

    except IOError as err:
        return str(err), 400

@app.route("/<path:path>")
def render_url(path):
    format = path[len(path)-3:]
    path = path[:len(path)-4]

    if format in ["dot", "gv"]:
        path = ".".join((path, format))
        format = "png"

    try:
        return response(path, format, **get_params(request))

    except IOError as err:
        return str(err), 400

def run():
    app.run(host='0.0.0.0', port=5001, debug=IS_DEV) # port doesn't work?
