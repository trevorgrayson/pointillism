from pytest import fixture
from point.models.repo import Repo


class TestRepo:
    @fixture
    def record(self):
        return {

        }

    @fixture
    def repo(self, record):
        return Repo(**record)

    def test_init(self, repo):
        assert isinstance(repo, Repo)

    # def test_requires_token(self, repo):
    #     assert not repo.requires_token

    # def test_label(self, repo):
    #     assert repo.label == '/'

    # def test_as_json(self, repo):
    #     pass
    #
    # def test_has_owner(self, repo):
    #     pass