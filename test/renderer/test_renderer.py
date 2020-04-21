from point.renderer import url

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
