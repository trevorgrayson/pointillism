from os import path
from config import THEME_DIR


class Theme:
    """
    name: str
    body: file pointer
    """
    def __init__(self, **attrs):
        self.name = attrs.get('name')
        self.body = attrs.get('body')


def read_theme(name):
    """
    read theme file

    Arguments:
        name: a theme's name
    Returns: Theme
    """
    filename = path.join(THEME_DIR, f"{name}.theme")

    with open(filename, 'r') as fp:
        return Theme(
            name=name,
            body=fp.read()
        )
