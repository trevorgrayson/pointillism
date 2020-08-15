import logging
from flask import request
from werkzeug.exceptions import Forbidden, InternalServerError, NotFound
from pybrake import Notifier

from .exceptions import PtNotFoundException
from config import (
    AIRBRAKE_PROJECT_ID, AIRBRAKE_API_KEY, ENV,
    airbrake_env, airbrake_enabled
)

notifier = None

if airbrake_enabled():
    notifier = Notifier(project_id=AIRBRAKE_PROJECT_ID,
                        project_key=AIRBRAKE_API_KEY,
                        environment=airbrake_env(ENV))


def add_exception_handling(app):
    if not airbrake_enabled():
        logging.info("Airbrake is not configured. Will not handle exceptions.")

    @app.errorhandler(NotFound)
    def error404(error):
        global notifier
        logging.exception(error)
        return "Not Found", 404

    @app.errorhandler(Forbidden)
    def error403(error):
        global notifier
        if airbrake_enabled():
            notifier.notify(error)
        return '{"message": "Upstream service rate limiting error. Please wait, and try again."}', 502

    @app.errorhandler(InternalServerError)
    def server_error(error):
        global notifier
        logging.exception(error)
        if airbrake_enabled():
            notifier.notify(error)
        raise error
