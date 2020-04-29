from point.models import GitHubRepo


class TestGithubRepo:
    def test_repo_owner(self):
        repo = GitHubRepo.first_repo('trevorgrayson', 'private')
        assert repo.owner == 'trevorgrayson'

    def test_repos_of(self):
        results = GitHubRepo.of('trevorgrayson')
        assert results != []
        assert len(results) >= 1
        result = results[0]
        assert result.name == 'private'
        assert result.label == 'trevorgrayson/private'
