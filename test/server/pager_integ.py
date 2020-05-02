from pytest import raises
from point.server import exception_handler


class TestPager:
    def test_airbrake(self):
        err = Exception("INTEG TEST: drats!")

        with raises(Exception):
            exception_handler(err)