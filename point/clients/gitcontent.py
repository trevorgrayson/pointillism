import requests
import logging
from os.path import join

LOG = logging.getLogger(__name__)
API_BASE = 'https://api.github.com'


class GithubException(Exception):
    pass


class NotAuthorized(GithubException):
    pass


class GitContent:
    def __init__(self, token=None):
        self.token = token

    def headers(self):
        heads = {
            'Accept': 'application/vnd.github.v3.raw'
        }

        if self.token is not None:
            heads['Authorization'] = f'token {self.token}'

        return heads

    def get(self, owner, repo, path):
        uri = join(API_BASE, 'repos', owner, repo, 'contents', path)
        print("IN HERE")
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
