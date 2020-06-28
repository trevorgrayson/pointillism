from os import environ, path, getcwd, urandom
import logging
import uuid

LOG_LEVEL = environ.get('LOG', environ.get('LOGLEVEL', 'INFO')).upper()
if not LOG_LEVEL:
    LOG_LEVEL = 'INFO'
print(f"Setting log level to {LOG_LEVEL}")
LOG_LEVEL = getattr(logging, LOG_LEVEL)
logging.basicConfig(level=LOG_LEVEL)

DOMAIN = environ.get('domain', 'pointillism.io')
HOST = environ['HOST']
ENV = environ.get('ENV', "PROD")

STATIC_DIR = getcwd()
THEME_DIR = environ.get("THEME_DIR", path.join(STATIC_DIR, "themes"))

if not STATIC_DIR or STATIC_DIR == '/':
    STATIC_DIR = '/srv/vhosts/pointillism'
else:
    STATIC_DIR += '/public'

SECRET_KEY = urandom(12)
# LDAP
LDAP_HOST = environ.get('LDAP_HOST')  

if LDAP_HOST is None:
    raise Exception("LDAP_HOST env var missing.")

# TODO 'ldap://openldap') ldap://users-service
LDAP_BASE_DN = environ.get('BASE_DN', "dc=ipsumllc,dc=com")

ADMIN_USER = environ.get('ADMIN_USER')
ADMIN_PASS = environ.get('ADMIN_PASS')

PLANT_JAR = environ.get("PLANT_JAR", "plantuml.jar")

#
# 3rd party
#
GITHUB_TOKEN = 'github_token'
GITHUB_CLIENT_ID = environ['GITHUB_CLIENT_ID']
GITHUB_SECRET = environ['GITHUB_SECRET']
GITHUB_STATE = str(uuid.uuid4()) # unique for each user
# authenticated users get 100x more requests
# TODO: if bath auth, does it fail?
DEFAULT_USER = 'pointillismio'

PAYPAL_CLIENT_ID = environ['PAYPAL_CLIENT_ID']

AIRBRAKE_PROJECT_ID = environ.get('AIRBRAKE_PROJECT_ID')
AIRBRAKE_API_KEY = environ.get('AIRBRAKE_API_KEY')


def airbrake_env(env):
    return {
        "PROD": 'production'
    }.get(env, 'development')