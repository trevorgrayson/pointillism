from models.base import GitHubUser


class TestGitHubUser:
    def test_create(self):
        results = GitHubUser.create('testuser', sn='testsn')
        assert results == True
