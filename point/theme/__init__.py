"""
Takes dot graph FILES and appends `themes`.
Dependent upon the dot graph language definition: https://www.graphviz.org/doc/info/lang.html
"""
import logging
from .reader import read_theme

LOG = logging.getLogger(__name__)
THEME = 'theme'


def theme_inject(dotfile, theme_name):
    """
    apply theme `theme_name` to dotfile.
    """
    if theme_name is None:
        return dotfile

    try:
        theme = read_theme(theme_name) # TODO cache these
    except IOError as err:
        LOG.error(f"Exception loading `{theme_name}` theme: {err}")
        return dotfile

    brace_pos = 0
    dot_def = ""

    for idx, c in enumerate(dotfile):
        if c == "{":
            brace_pos = idx
            break
        else:
            dot_def += c

    return dot_def + "{\n" + theme.body + "\n" + dotfile[brace_pos+1:]
