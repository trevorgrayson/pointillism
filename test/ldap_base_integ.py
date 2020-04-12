from models.base import GitHubRepo, GitHubUser


class TestLDIFRecord:
    def test_create(self):
        results = GitHubRepo.create('trevorgrayson', 'private3')

        assert results == True

    def test_create_on_user(self):
        user = GitHubUser.create('bob', sn='bob')
        results = GitHubRepo.create('bob', 'private5', base_dn='cn=bob')

        assert results == True

    def test_search(self):
        results = GitHubRepo.search('private3')

        print(results)

