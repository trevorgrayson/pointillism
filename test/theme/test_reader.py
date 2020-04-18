from point.theme.reader import read_theme, Theme

A_THEME_NAME = 'default'


class TestReader:
    def test_read_theme(self):
        theme = read_theme(A_THEME_NAME)

        assert isinstance(theme, Theme)
        assert theme.name == 'default'
        assert theme.body is not None
        assert theme.body.startswith('rankdir=BT')
