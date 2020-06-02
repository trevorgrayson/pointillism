from pytest import fixture, mark
from point.clients.gitcontent import GitContent
from point.models import User
from os import environ

GIT_TOKEN = environ['GIT_TOKEN']

class TestGitContent:
    @fixture
    def user(self):
        return User(git_token=[GIT_TOKEN])

    def test_init(self, user):
        client = GitContent(user)
        dot = client.get('trevorgrayson', 'pointillism', 'master', '/example.dot')
        assert dot is not None

    def test_private(self, user):
        client = GitContent(user)
        dot = client.get('trevorgrayson', 'private', 'master', '/example.dot')
        assert dot[:7] == 'digraph'

    def test_private_token(self, user):
        client = GitContent(GIT_TOKEN)
        dot = client.get('trevorgrayson', 'private', 'master', '/example.dot')
        assert dot[:7] == 'digraph'

    @mark.parametrize('org, repo, expect', [
        ('aslkjf9233', 'missing-324230491', None),
        ('trevorgrayson', 'pointillism', 'trevorgrayson'),
        ('trevorgrayson', 'private', 'trevorgrayson'),
        ('openfireproj', 'private', None)
    ])
    def test_exists(self, user, org, repo, expect):
        client = GitContent(user)
        owner = client.owner(org, repo)
        assert owner == expect
