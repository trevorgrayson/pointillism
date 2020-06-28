import logging
import subprocess
from io import StringIO
from point.renderer.exceptions import RenderFailure
from config import PLANT_JAR

FORMATS = ['svg', 'png', 'pdf', 'vdx', 'eps']


def plant_args(format):
    return [
        '/usr/bin/java', '-jar', PLANT_JAR, "-p",
        f"-t{format.lower()}"
    ]


def get_pipe(body, format):
    if format not in FORMATS:
        raise RenderFailure(f"PlantUML cannot render {format}")

    proc = subprocess.Popen(plant_args(format), bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)  # stderr
    result, err = proc.communicate(input=f"{body}".encode())
    logging.debug(f"PlantUML response: {result}")
    logging.debug(f"PlantUML err: {err}")
    if err is None:
        return result.decode('utf8')
    else:
        raise RenderFailure(f"PlantUML Process: {err}")
