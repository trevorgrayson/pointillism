import requests
from flask import Blueprint, redirect, request, make_response
from config import GITHUB_TOKEN, GITHUB_CLIENT_ID, GITHUB_SECRET, GITHUB_STATE
from ldapauth import LdapAuth
from config import LDAP_HOST, LDAP_BASE_DN, ADMIN_USER, ADMIN_PASS

GIT_WEBHOOK_AUTH = '/github/auth'

API_HOST = 'https://api.github.com'

class GitHubAuth:
    def __init__(self, host='https://github.com',
                 **creds):
        self.host = host
        self.client_id = creds.get('client_id')
        self.secret = creds.get('secret')
        self.scope = creds.get('scope', 'repo')

    def login(self):
        params = dict(
            client_id=self.client_id,
            redirect_url=GIT_WEBHOOK_AUTH,
            scope=self.scope,
            state=GITHUB_STATE
        )
        query = "&".join([f'{k}={v}' for k, v in params.items()])
        return f'{self.host}/login/oauth/authorize?{query}'

    def auth_webhook(self, code, state=None):
        # if state == GITHUB_STATE:
        params = dict(
            client_id=self.client_id,
            client_secret=self.secret,
            code=code,
        )
        response = requests.post(f'{self.host}/login/oauth/access_token',
                                 json=params, headers=self.headers)

        if response.status_code == 200:
            auth = response.json()
            return auth
        else:
            raise Exception(f'Upstream service exception: {response.status_code}')

    @property
    def headers(self):
        return {
            'Accept': 'application/json'
        }

    @classmethod
    def get(cls, path, token):
        response = requests.get(path, headers=cls.auth_headers(token))

        if response.status_code == 200:
            return response.body
        else:
            raise Exception(f'Upstream service exception: {response.status_code}')

    @classmethod
    def me(cls, token):
        response = requests.get(f'{API_HOST}/user', headers=cls.auth_headers(token))

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Upstream service exception: {response.status_code}')

    @classmethod
    def auth_headers(cls, token):
        return {
            'Authorization':  f'token {token}',
            'Accept': 'application/json'
        }


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
