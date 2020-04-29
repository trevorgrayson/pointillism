from flask import Blueprint, redirect, request, make_response
from config import GITHUB_CLIENT_ID, GITHUB_SECRET

from point.clients.githubauth import GitHubAuth
from ldapauth import LdapAuth
from config import LDAP_HOST, ADMIN_USER, ADMIN_PASS, LDAP_BASE_DN
from point.models.user import GIT_TOKEN, PT_SESSION_TOKEN


gitclient = GitHubAuth(client_id=GITHUB_CLIENT_ID,
                       secret=GITHUB_SECRET)


github_routes = Blueprint('github_routes', __name__)


@github_routes.route('/')
def welcome():
    return 'github avail!'


@github_routes.route('/login')
def login():
    return redirect(gitclient.login())
    

@github_routes.route('/auth')
def auth():
    code = request.args.get('code')
    state = request.args.get('state')
    if code is None:
        return 400, "missing github `code`"
    # if code is not ...

    ldapclient = LdapAuth(LDAP_HOST, LDAP_BASE_DN, ADMIN_USER, ADMIN_PASS)
    event = gitclient.auth_webhook(code, state)
    token = event.get('access_token')
    if token is None:
        return '{"message": "token not found."}', 400

    # get or create user
    github_user = GitHubAuth.me(token)
    github_login = github_user['login']
    user = ldapclient.search(username=github_login)
    # save auth id
    if len(user) == 0:
        # prompt user for name?
        user = ldapclient.create(github_login)
    else:
        user = user[0]

    user.attributes = {GIT_TOKEN: token}
    ldapclient.update(user)

    response = make_response(redirect('/'))
    response.set_cookie(PT_SESSION_TOKEN, token)

    return response


@github_routes.route('logout')
def logout():
    response = make_response(redirect('/'))
    response.set_cookie(PT_SESSION_TOKEN, '', expires=0)

    return response
