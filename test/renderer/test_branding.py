from point.renderer.render import get_pipe
from point.renderer.branding import brand

# TODO shared fixtures
BODY = """
digraph Test {
    A -> {B, C, D}
}
"""


class TestBranding:
    def test_url(self):
        body = get_pipe(BODY, format="svg")
        assert 'pointillism.io' in body
