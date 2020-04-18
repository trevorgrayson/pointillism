from point.theme import theme

DOT_FILE = "digraph Bob { A -> B }"


class TestTheme:
    def test_theme(self):
        result = theme(DOT_FILE, 'default')

        assert "digraph Bob {" in result
        assert "rankdir=BT" in result
        assert "A -> B" in result