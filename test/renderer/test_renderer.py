from point.renderer import (
    url, get_mime, cache_control
)

HOST = 'http://lolcatsho.local'


class TestRenderer:
    def test_url(self):
        path = 'bob/uncle' 
        params = {
            'param1': 'value1',
            'param2': 'value2'
        }

        result = url(HOST, path, **params)
        assert result == 'http://lolcatsho.local/bob/uncle?param1=value1&param2=value2'

    def test_get_mime(self):
        assert get_mime('svg') == 'svg+xml'

    def test_cache_control(self):
        headers = cache_control()
        assert headers['cache-control'] == 'max-age=0 private'

    def test_render(self):
        pass
