from os import environ
from pytest import fixture
from requests import get

TOKEN = environ['GIT_TOKEN']

class TestSmoke:

    @fixture
    def host(self):
        return environ.get('TEST_HOST', 'http://localhost:5001')

    def test_pu_default(self, host):
        # /trevorgrayson/pointillism/ac7b6c71098fce9c2012a686a47c6feb5767a8bf/plant/sequence.pu
        # /trevorgrayson/pointillism/ac7b6c71098fce9c2012a686a47c6feb5767a8bf/plant/sequence.pu.svg
        # /trevorgrayson/pointillism/ac7b6c71098fce9c2012a686a47c6feb5767a8bf/plant/sequence.pu.png
        response = get(host + '/trevorgrayson/pointillism/master/example.dot.svg')
        assert response.status_code == 200

