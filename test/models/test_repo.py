from pytest import fixture
from point.models.repo import Repo


class TestRepo:
    @fixture
    def record(self):
        return {}

    @fixture
    def repo(self, record):
        return Repo(**record)

    def test_init(self, repo):
        assert isinstance(repo, Repo)
