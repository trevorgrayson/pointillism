from point.theme import theme_inject

DOT_FILE = "digraph Bob { A -> B }"


class TestTheme:
    def test_theme(self):
        result = theme_inject(DOT_FILE, 'default')

        assert "digraph Bob {" in result
        assert "rankdir=BT" in result
        assert "A -> B" in result