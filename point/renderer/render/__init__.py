import logging
from .dot import get_pipe as dot_pipe
from .plantuml import get_pipe as plant_pipe

from config import WILL_BRAND

from point.renderer.branding import brand, is_brandable_format


def is_plantuml(body):
    return body[0] == '@'


def get_pipe(body, format):
    """abstracts getting pipe from multiple rendering libraries

    returns:
    """
    renderer = dot_pipe
    if is_plantuml(body):
        logging.debug("Electing to render PlantUML")
        renderer = plant_pipe

    resp = renderer(body, format)

    if WILL_BRAND and is_brandable_format(format):
        resp = brand(resp)

    return resp