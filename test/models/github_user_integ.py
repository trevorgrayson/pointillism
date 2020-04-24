from point.models import GitHubUser, User


class TestGitHubUser:
    """
    NOTE: NOT ASYNC COMPAT
    """
    def test_create(self):
        cn = 'testuser'
        create_result = GitHubUser.create('testuser', sn='testsn')

        user = GitHubUser.first(cn)

        assert create_result == True
        assert isinstance(user, User)
        assert isinstance(user.token, str)

    def test_first(self):
        results = GitHubUser.first('trevorgrayson')
        assert results.name == 'trevorgrayson'

    def test_delete(self):
        testuser = GitHubUser.first('testuser')
        assert GitHubUser.delete(testuser)
