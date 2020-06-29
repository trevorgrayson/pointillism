from os import environ
from pytest import fixture
from requests import get

TOKEN = environ['GIT_TOKEN']

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
        response = get(host + '/trevorgrayson/private/master/example.dot.svg?token=' + TOKEN)
        assert response.status_code == 200

    def test_private_no_fmt(self, host):
        response = get(host + '/trevorgrayson/private/master/example.dot?token=' + TOKEN)
        assert response.status_code == 200

    def test_404(self, host):
        response = get(host + '/trevorgrayson/pointillism/master/not-here-file.dot.svg')
        assert response.status_code == 404
        assert 'https://github.com/trevorgrayson/pointillism/master/not-here-file.dot' in response.text


# http://localhost:5001/github/trevorgrayson/private/master/example.dot.svg?token=7ac69c88-259e-4c24-858f-dda7fdcb9765


# https://raw.githubusercontent.com/trevorgrayson/private/master/example.dot?token=AAAHCI6RNBEWMRPUTQHFCBK6VHC42
