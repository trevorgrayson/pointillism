from models import GitHubUser


class TestGitHubUser:
    def test_create(self):
        results = GitHubUser.create('testuser', sn='testsn')
        assert results == True

    def test_first(self):
        results = GitHubUser.first('trevorgrayson')
        assert results.name == 'trevorgrayson'
