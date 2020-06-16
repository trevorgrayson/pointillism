from pytest import fixture
from point.models import GitResource


class TestRepo:
    @fixture
    def record(self):
        return {}

    @fixture
    def resource(self, record):
        return GitResource(**record)

    def test_init(self, resource):
        assert isinstance(resource, GitResource)

    def test_parse(self):
        resource = GitResource.parse('http://pointillism.io/trevorgrayson/pointillism/master/example.dot')

        assert resource.owner == 'trevorgrayson'
        assert resource.project == 'pointillism'

    def test_str(self):
        resource = GitResource.parse('http://pointillism.io/trevorgrayson/pointillism/master/example.dot')
        assert str(resource) == 'https://github.com/trevorgrayson/pointillism/blob/None/master/example.dot'
