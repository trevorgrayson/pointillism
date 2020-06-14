import logging
from flask import request
from werkzeug.exceptions import Forbidden, InternalServerError, NotFound
from pybrake import Notifier

from config import AIRBRAKE_PROJECT_ID, AIRBRAKE_API_KEY, airbrake_env, ENV
from .exceptions import PtNotFoundException

notifier = Notifier(project_id=AIRBRAKE_PROJECT_ID,
                    project_key=AIRBRAKE_API_KEY,
                    environment=airbrake_env(ENV))


def add_exception_handling(app):

    @app.errorhandler(NotFound)
    def error404(error):
        logging.exception(error)
        notifier.notify(PtNotFoundException(
            f"Not Found: {request.path}"
        ))
        raise error

    @app.errorhandler(Forbidden)
    def error403(error):
        notifier.notify(error)
        return '{"message": "Rate limiting error. Please wait, and try again."}', 502

    @app.errorhandler(InternalServerError)
    def server_error(error):
        notifier.notify(error)
        raise error
