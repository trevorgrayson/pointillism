from pytest import fixture
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
