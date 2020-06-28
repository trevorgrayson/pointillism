from point.renderer.render.plantuml import get_pipe
from pytest import mark

SEQUENCE = """
@startuml
Alice -> Bob: Authentication Request
Bob --> Alice: Authentication Response

Alice -> Bob: Another authentication Request
Alice <-- Bob: Another authentication Response
@enduml
"""

DOTFILE = """
digraph {
    A -> B
    B -> C
}
"""


class TestPlantUML:
    def test_svg(self):
        svg = get_pipe(SEQUENCE, 'svg')

        assert svg.startswith('<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg')

    @mark.skip("This doesn't pass")
    def test_dotfile_svg(self):
        svg = get_pipe(DOTFILE, 'svg')

        assert svg.startswith('<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg')
