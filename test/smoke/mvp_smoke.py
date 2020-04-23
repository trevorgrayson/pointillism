from os import environ
from pytest import fixture
from requests import get


class TestSmoke:

    @fixture
    def host(self):
        return environ.get('TEST_HOST', 'http://localhost:5001')

    def test_mvp(self, host):
        response = get(host + '/trevorgrayson/pointillism/master/example.dot.svg')
        assert response.status_code == 200

    def test_github(self, host):
        response = get(host + '/github/trevorgrayson/pointillism/master/example.dot.svg')
        assert response.status_code == 200

    def test_private(self, host):
        response = get(host + '/trevorgrayson/private/master/example.dot.svg')
        assert response.status_code == 200

    def test_404(self, host):
        response = get(host + '/trevorgrayson/pointillism/master/not-here-file.dot.svg')
        assert response.status_code == 404
