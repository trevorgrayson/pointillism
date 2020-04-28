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

    def test_find_by_email(self):
        results = GitHubUser.find(email="trevor@trevorgrayson.com")

        assert len(results) > 0
        user = results[0]
        assert user.cn == 'trevorgrayson'