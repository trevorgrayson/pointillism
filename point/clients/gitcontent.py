from base64 import b64decode
import logging
from os.path import join
from github import Github
from config import GITHUB_CLIENT_ID, GITHUB_SECRET

LOG = logging.getLogger(__name__)


class GitContent:
    def __init__(self, creds=None):
        if hasattr(creds, 'git_token'):
            creds = creds.git_token

        self.github = Github(login_or_token=creds, client_id=GITHUB_CLIENT_ID,
                             client_secret=GITHUB_SECRET)

    def get(self, owner, repo, branch, path):
        repo = self.github.get_repo(f'{owner}/{repo}', lazy=False)
        return b64decode(repo.get_contents(path).content).decode('utf-8')
