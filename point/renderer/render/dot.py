from graphviz import Source


def get_pipe(body, format):
    src = Source(body)
    return src.pipe(format=format)
