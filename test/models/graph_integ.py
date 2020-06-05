from pytest import fixture
from point.models import Graph, GraphDAO, GitHubRepo


class TestGraph:
    @fixture
    def repo(self):
        return GitHubRepo.first('trevorgrayson', 'private')

    def test_create(self, repo):
        assert GraphDAO.create(repo, 'trevorgrayson', 'example.dot')

    def test_search(self, repo):
        graphs = GraphDAO.find('trevorgrayson', 'trevorgrayson', 'private')
        assert len(graphs) == 1
