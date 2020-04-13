from models import GitHubRepo


class TestGithubRepo:
    def test_repo_credentials(self):
        repo = GitHubRepo.first_repo('trevorgrayson', 'private')

        print(repo.credentials)
