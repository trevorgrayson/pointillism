from models import GitHubRepo


class TestGithubRepo:
    def test_repo_owner(self):
        repo = GitHubRepo.first_repo('trevorgrayson', 'private')
        assert repo.owner == 'trevorgrayson'
