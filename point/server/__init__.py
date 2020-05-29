import logging as log
from json import dumps
from flask import Flask, request, g, session
from string import Template
from flask_simpleldap import LDAP

from .errors import add_exception_handling, notifier
from .github import github_routes
# from .repos import repo_routes
from .api.v1 import v1_routes
from .paypal import paypal_routes

from .utils import headers, RegexConverter, response, parse_request_fmt, parse_request_path
from point.models import GitHubRepo, GitHubUser, GitResource
from point.server.base import get_me
from point.clients.gitcontent import GitContent
from point.renderer import render, cache_control
from ldapauth.flask.routes import auth_routes, register_config
from github import GithubException

from config import (ADMIN_USER, ADMIN_PASS, LDAP_BASE_DN, SECRET_KEY,
                    DOMAIN, HOST, ENV, STATIC_DIR, PAYPAL_CLIENT_ID, LDAP_HOST)

app = Flask(__name__)
add_exception_handling(app)
app.register_blueprint(github_routes, url_prefix='/github')
app.register_blueprint(v1_routes, url_prefix='/v1')
app.register_blueprint(auth_routes)
# app.register_blueprint(repo_routes)
app.register_blueprint(paypal_routes)

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

DOT_FORMATS = ["dot", "gv"]


@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        # This is where you'd query your database to get the user info.
        g.user = get_me()
        # Create a global with the LDAP groups the user is a member of.
        # g.ldap_groups = ldap.get_user_groups(user=session['username'])


IS_DEV = (ENV == "develop")


@app.route("/paypal/confirm")
@app.route("/profile")
@app.route("/account")
@app.route("/repos")
@app.route("/getting-started")
@app.route("/about")
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


@app.route("/<string:org>/<string:project>/blob/<string:branch>/<path:path>")
@app.route("/github/<string:org>/<string:project>/<string:branch>/<path:path>")
@app.route("/<string:org>/<string:project>/<string:branch>/<path:path>")
def render_github_url(org, project, branch, path):
    log.debug("REQUEST /github: {path}")
    resource = GitResource(org, project, branch, path)
    fmt = parse_request_fmt(path)
    path = parse_request_path(path)
    public = True
    creds = request.args.get('token')
    render_params = {
        "theme": request.args.get('theme'),
        "format": fmt[1:]
    }

    repo = GitHubRepo.first_repo(org, project)

    def is_allowed(repo, token):
        return repo and repo.has_owner and \
            repo.requires_token and \
            repo.token == token

    if is_allowed(repo, request.args.get('token')):
        log.debug(f"Authenticated as {repo.owner}")
        owner = GitHubUser.first(repo.owner)
        creds = owner
        public = False
    log.debug(repo)

    try:
        log.debug(f"fetching {resource}")
        body = GitContent(creds).get(org, project, branch, path)
        resp = render(body, **render_params)
        resp.headers = cache_control(public, resp.headers)
        return resp
    except GithubException as err:
        log.error(err)
        notifier.notify(err)
        return dumps({
            'message': f"Exception finding document: {resource}. " +\
            'Is the repository private? Do you need a valid token?'
        }), 404


def run():
    app.run(host='0.0.0.0', port=5001, debug=IS_DEV)
