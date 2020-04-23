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
from point.clients.gitcontent import GitContent, GithubException
from point.renderer import render

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
        g.user = get_me()
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
    # GitHubRepo.first_repo(org, name)

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


@app.route("/github/<path:path>")
def render_github_url(path):
    LOG.debug("REQUEST /github: {path}")
    # BUG: don't want to require owner to load first. or do you?
    org, project, branch, *tail = path.split('/')
    path = '/'.join(tail)
    path = path[:len(path)-4]
    token = None

    repo = GitHubRepo.first_repo(org, project)
    if repo and repo.has_owner:
        if repo.requires_token and \
          repo.token is not None and \
          repo.token != request.args.get('token'):
            return '{"message": "Unauthorized. Provide repo `token` param"}', 401

        owner = GitHubUser.first(repo.owner)
        token = owner.git_token

    try:
        body = GitContent(token).get(org, project, path)
        return render(body)
    except GithubException as err:
        LOG.error(err)
        return "Not Found.", 404


@app.route("/<path:path>")
def render_url(path):
    LOG.debug("REQUEST /root: {path}")
    org, project, branch, *tail = path.split('/')
    path = '/'.join(tail)
    path = path[:len(path) - 4]
    token = None

    repo = GitHubRepo.first_repo(org, project)
    if repo and repo.has_owner:
        if repo.requires_token and \
                repo.token is not None and \
                repo.token != request.args.get('token'):
            return '{"message": "Unauthorized. Provide repo `token` param"}', 401

        owner = GitHubUser.first(repo.owner)
        token = owner.git_token

    try:
        body = GitContent(token).get(org, project, path)
        return render(body)
    except GithubException as err:
        LOG.error(err)
        return "Not Found.", 404
    # format = path[len(path)-3:]
    # path = path[:len(path)-4]
    #
    # if format in ["dot", "gv"]:
    #     path = ".".join((path, format))
    #     format = "png"
    #
    # params = get_params(request)
    # if headers:
    #     params['headers'] = headers
    # try:
    #     return response(path, format, **params)
    #
    # except IOError as err:
    #     return str(err), 400


def run():
    app.run(host='0.0.0.0', port=5001, debug=IS_DEV)
