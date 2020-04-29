import requests
import logging
from os.path import join

LOG = logging.getLogger(__name__)
API_BASE = 'https://api.github.com'
RAW_BASE = 'https://raw.githubusercontent.com'


class GithubException(Exception):
    pass


class NotAuthorized(GithubException):
    pass


class GitContent:
    def __init__(self, creds=None):
        self.creds = creds

    def headers(self):
        heads = {
            'Accept': 'application/vnd.github.v3.raw'
        }

        if hasattr(self.creds, 'git_token'):
            heads['Authorization'] = f'token {self.creds.git_token}'

        return heads

    def get(self, owner, repo, branch, path):
        uri = join(API_BASE, 'repos', owner, repo, 'contents', path)
        if isinstance(self.creds, str):
            uri = join(RAW_BASE, owner, repo, branch, path) + f'?token={self.creds}'
        LOG.info(uri)
        LOG.info(self.headers())
        response = requests.get(uri, headers=self.headers())
        # TODO if 200
        if response.status_code in [401, 403]:
            raise NotAuthorized(response.text)
        elif response.status_code == 200:
            return response.text
        else:
            raise GithubException(response.text)
