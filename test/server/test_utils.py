from pytest import mark
from point.server.utils import parse_request_fmt, parse_request_path, convert


class TestUtils:
    @mark.parametrize('path, expected', {
        ("/example.gv", ".svg"),
        ("/example.dot", ".svg"),
        ("/example.dot.svg", ".svg"),
        ("/example.dot.png", ".png"),
        ("/example.dot.pdf", ".pdf"),
        ("/with/dir/example.dot.pdf", ".pdf")
    })
    def test_request_fmt(self, path, expected):
        assert parse_request_fmt(path) == expected

    @mark.parametrize('path, expected', {
        ("/example.gv", "/example.gv"),
        ("/example.dot", "/example.dot"),
        ("/example.dot.svg", "/example.dot"),
        ("/example.dot.png", "/example.dot"),
        ("/example.dot.pdf", "/example.dot"),
        ("/with/dir/example.dot.pdf", "/with/dir/example.dot")
    })
    def test_get_path(self, path, expected):
        assert parse_request_path(path) == expected

    @mark.parametrize('org, project, branch, path, creds, expected', {
        ('ipsum', 'proj', 'branch', '/example.gv', None,
         'https://pointillism.io/ipsum/proj/branch/example.gv'),
        ('ipsum', 'private', 'master', '/example.dot', 'sometoken',
         'https://pointillism.io/ipsum/private/master/example.dot?token=sometoken')
    })
    def test_convert(self, org, project, branch, path, creds, expected):
        assert convert(org, project, branch, path.lstrip('/'), creds) == expected