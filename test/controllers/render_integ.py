from pytest import fixture
from json import dumps
from point.server import app


class TestRender:
    @fixture
    def client(self):
        return app.test_client()

    def test_welcome(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_render(self, client):
        response = client.get('/trevorgrayson/pointillism/master/example.dot.svg')
        assert response.status_code == 200

    def test_render(self, client):
        response = client.get('/trevorgrayson/pointillism/master/example-not-exist.dot.svg')
        assert response.status_code == 404

    def test_convert(self, client):
        url = 'https://github.com/trevorgrayson/pointillism/blob/master/example.dot'
        response = client.post(
            '/convert',
            headers={'content-type': 'application/json'},
            data=dumps({'url': url})
        )
