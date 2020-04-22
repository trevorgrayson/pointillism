import logging
from flask import Flask, request, g, session
from string import Template

from urllib.parse import urlparse
from config import DOMAIN, HOST, ENV, STATIC_DIR, PAYPAL_CLIENT_ID, LDAP_HOST
from point.server.github import github_routes
from point.server.repos import repo_routes
from point.server.api.v1 import v1_routes
from point.models import GitHubRepo, GitHubUser

from config import ADMIN_USER, ADMIN_PASS, LDAP_BASE_DN, SECRET_KEY
from ldapauth.flask.routes import auth_routes, register_config
from .utils import headers, RegexConverter, response
from point.server.base import get_me
from flask_simpleldap import LDAP

LOG = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(github_routes, url_prefix='/github')
app.register_blueprint(v1_routes, url_prefix='/v1')
app.register_blueprint(auth_routes)
app.register_blueprint(repo_routes)

register_config(app,
                ldap_host=LDAP_HOST,
                ldap_base_dn=LDAP_BASE_DN,
                ldap_username=ADMIN_USER,
                ldap_password=ADMIN_PASS,
                ldap_login_view='auth.login'
                )
app.config['SECRET_KEY'] = SECRET_KEY
app.url_map.converters['regex'] = RegexConverter

ldap = LDAP()


@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        # This is where you'd query your database to get the user info.
        g.user = {}
        # Create a global with the LDAP groups the user is a member of.
        # g.ldap_groups = ldap.get_user_groups(user=session['username'])


IS_DEV = (ENV == "develop")


def get_params(request):
    params = {
        'theme': request.args.get('theme')
    }

    # if authorized
    # has resource token
    # TODO include token from account

    if 'token' in request.args:
        params['token'] = request.args['token']

    return params


@app.route("/")
def welcome():
    me = get_me()
    username = ''
    if me:
        username = me.cn

    with open(STATIC_DIR + '/index.html', 'r') as fp:
        template = Template(fp.read())

        return template.substitute(
            host=HOST,
            domain=DOMAIN,
            paypalId=PAYPAL_CLIENT_ID,
            username=username
        )


@app.route("/rel/<path:path>")
def render_relative_path(path):
    """ Find the path on the referring host's server """
    format = path[len(path)-3:]
    path = path[:len(path)-4]
    referrer = request.referrer or None
    if referrer is None:
        return "No referring URL.", 404

    host = urlparse(referrer).hostname

    if format in ["dot", "gv"]:
        path = ".".join((path, format))
        format = "png"

    try:
        return response(path, format, host=host, **get_params(request))

    except IOError as err:
        return str(err), 400


@app.route("/.<path:path>\.<regex(\"[a-zA-Z0-9]{3}\"):fileFormat>\.<regex(\"[a-zA-Z0-9]{3}\"):format>")
def render_url_with_format(path):
    if format == 'dot': # no filename, use default
      render_url(".".join((path, fileFormat, "png")))


@app.route("/github/<path:path>")
def render_github_url(path):
    # BUG: don't want to require owner to load first. or do you?
    org, project, *_tail = path.split('/')

    repo = GitHubRepo.first_repo(org, project)
    owner = None

    if repo and repo.has_owner:
        owner = GitHubUser.first(repo.owner)

    return render_url(path, headers=headers(user=owner))


@app.route("/<path:path>")
def render_url(path, headers=None, **kwargs):
    format = path[len(path)-3:]
    path = path[:len(path)-4]

    if format in ["dot", "gv"]:
        path = ".".join((path, format))
        format = "png"

    params = get_params(request)
    if headers:
        params['headers'] = headers
    try:
        return response(path, format, **params)

    except IOError as err:
        return str(err), 400


def run():
    app.run(host='0.0.0.0', port=5001, debug=IS_DEV)
