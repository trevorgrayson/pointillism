import requests
from flask import Blueprint, redirect, request, make_response
from config import GITHUB_TOKEN, GITHUB_CLIENT_ID, GITHUB_SECRET, GITHUB_STATE

GIT_WEBHOOK_AUTH = '/github/auth'

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
        response = requests.get(path, cls.auth_headers(token))

        if response.status_code == 200:
            return response.body
        else:
            raise Exception(f'Upstream service exception: {response.status_code}')

    @classmethod
    def auth_headers(cls, token):
        return {
            'Authorization':  f'token {token}'
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
    
    auth = client.auth_webhook(code, state)

    # TODO redirect to where?
    response = make_response(redirect('/github'))
    response.set_cookie(GITHUB_TOKEN, auth['access_token'])

    return response
    # TODO if token in cookie, append to request
