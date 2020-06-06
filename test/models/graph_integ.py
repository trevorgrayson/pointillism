from pytest import fixture
from point.models.graph import Graph, GraphDAO
from point.models import GitHubRepo


class TestGraph:
    @fixture
    def repo(self):
        return GitHubRepo.first('trevorgrayson', 'pointillism')

    def test_create(self, repo):
        assert GraphDAO.create(repo, 'trevorgrayson', 'blob/master/example.dot')

    def test_search(self, repo):
        graphs = GraphDAO.find('trevorgrayson', 'trevorgrayson', 'pointillism')
        graph = graphs[0]

        assert len(graphs) == 1
        assert graph.url == '/trevorgrayson/pointillism/blob/master/example.dot'
