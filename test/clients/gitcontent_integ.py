from pytest import fixture
from point.clients.gitcontent import GitContent
from point.models import User


class TestGitContent:
    @fixture
    def user(self):
        return User(git_token=["fb8aaeafffc4b327cefe17d4f32c242bcebfa79a"])

    def test_init(self, user):
        client = GitContent(user)
        dot = client.get('trevorgrayson', 'pointillism', 'master', '/example.dot')
        assert dot is not None

    def test_private(self, user):
        client = GitContent(user)
        dot = client.get('trevorgrayson', 'private', 'master', '/example.dot')
        assert dot[:7] == 'digraph'

    def test_private_token(self, user):
        client = GitContent('fb8aaeafffc4b327cefe17d4f32c242bcebfa79a')
        dot = client.get('trevorgrayson', 'private', 'master', '/example.dot')
        assert dot[:7] == 'digraph'
