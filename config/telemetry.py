from os import environ


AIRBRAKE_PROJECT_ID = environ.get('AIRBRAKE_PROJECT_ID')
AIRBRAKE_API_KEY = environ.get('AIRBRAKE_API_KEY')


def airbrake_env(env):
    return {
        "PROD": 'production'
    }.get(env, 'development')


def airbrake_enabled():
    return AIRBRAKE_API_KEY is not None
