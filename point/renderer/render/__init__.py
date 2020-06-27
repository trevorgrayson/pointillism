from .dot import get_pipe as dot_pipe


def get_pipe(body, format):
    """abstracts getting pipe from multiple rendering libraries"""
    return dot_pipe(body, format)