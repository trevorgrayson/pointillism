from werkzeug.exceptions import Forbidden, InternalServerError
from pybrake import Notifier

from config import AIRBRAKE_PROJECT_ID, AIRBRAKE_API_KEY, airbrake_env, ENV

notifier = Notifier(project_id=AIRBRAKE_PROJECT_ID,
                    project_key=AIRBRAKE_API_KEY,
                    environment=airbrake_env(ENV))


def add_exception_handling(app):

    @app.errorhandler(Forbidden)
    def error403(error):
        notifier.notify(error)
        return '{"message": "Rate limiting error. Please wait, and try again."}', 502

    @app.errorhandler(InternalServerError)
    def server_error(error):
        notifier.notify(error)
        raise error
