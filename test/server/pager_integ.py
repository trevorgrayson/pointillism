from pytest import raises, mark
from point.server.errors import add_exception_handling


class TestPager:
    @mark.skip("broken")
    def test_airbrake(self):
        err = Exception("INTEG TEST: drats!")

        with raises(Exception):
            exception_handler(err)