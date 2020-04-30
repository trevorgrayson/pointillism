from base64 import b64decode
import logging
from os.path import join
from github import Github

LOG = logging.getLogger(__name__)


class GitContent:
    def __init__(self, creds=None):
        if hasattr(creds, 'git_token'):
            self.github = Github(creds.git_token)
        else:
            self.github = Github(creds)

    def get(self, owner, repo, branch, path):
        repo = self.github.get_repo(f'{owner}/{repo}')
        return b64decode(repo.get_contents(path).content).decode('utf-8')
