from .dot import get_pipe as dot_pipe
from .plantuml import get_pipe as plant_pipe


def is_plantuml(body):
    return body[0] == '@'


def get_pipe(body, format):
    """abstracts getting pipe from multiple rendering libraries"""
    renderer = dot_pipe
    if is_plantuml(body):
        renderer = plant_pipe

    return renderer(body, format)