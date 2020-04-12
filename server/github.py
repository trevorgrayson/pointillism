from flask import Blueprint, redirect, request, make_response
from config import GITHUB_TOKEN, GITHUB_CLIENT_ID, GITHUB_SECRET, GITHUB_STATE

from .githubauth import GitHubAuth

client = GitHubAuth(client_id=GITHUB_CLIENT_ID, 
                    secret=GITHUB_SECRET)


github_routes = Blueprint('github_routes', __name__)


@github_routes.route('/')
def welcome():
    return 'github avail!'


@github_routes.route('/login')
def login():
    return redirect(client.login())
    

@github_routes.route('/auth')
def auth():
    code = request.args.get('code')
    state = request.args.get('state')
    if code is None:
        return 400, "missing github `code`"

    USERS = LdapAuth(LDAP_HOST, LDAP_BASE_DN, ADMIN_USER, ADMIN_PASS)
    auth = client.auth_webhook(code, state)
    token = auth['access_token']

    # get or create user
    github_user = GitHubAuth.me(token)
    github_login = github_user['login']
    user = USERS.search(username=github_login)
    # save auth id
    if len(user) == 0:
        # prompt user for name?
        user = USERS.create(github_login)
    else:
        user = user[0]

    user.attributes = {'givenName': token}
    USERS.update(user)

    response = make_response(redirect('/github'))
    # TODO give them a pointillism account id
    response.set_cookie(GITHUB_TOKEN, token)

    return response
    # TODO if token in cookie, append to request
