import logging
import requests
from config import GITHUB_STATE

LOG = logging.getLogger(__name__)
GIT_WEBHOOK_AUTH = '/github/auth'
API_HOST = 'https://api.github.com'


class GitHubAuth:
    def __init__(self, host='https://github.com',
                 **creds):
        self.host = host
        self.client_id = creds.get('client_id')
        self.secret = creds.get('secret')
        self.scope = creds.get('scope', 'repo,user:email')

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
            LOG.info(auth)
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
