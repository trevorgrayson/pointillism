from os import environ, path, getcwd, urandom
import logging
import uuid

from .auth import *
from .telemetry import *

LOG_LEVEL = environ.get('LOG', environ.get('LOGLEVEL', 'INFO')).upper()
if not LOG_LEVEL:
    LOG_LEVEL = 'INFO'
print(f"Setting log level to {LOG_LEVEL}")
LOG_LEVEL = getattr(logging, LOG_LEVEL)
logging.basicConfig(level=LOG_LEVEL)

DOMAIN = environ.get('domain', 'pointillism.io')
HOST = environ.get('HOST', 'https://raw.githubusercontent.com')
ENV = environ.get('ENV', "PROD")

STATIC_DIR = getcwd()
THEME_DIR = environ.get("THEME_DIR", path.join(STATIC_DIR, "themes"))

if not STATIC_DIR or STATIC_DIR == '/':
    STATIC_DIR = '/srv/vhosts/pointillism'
else:
    STATIC_DIR += '/public'

SECRET_KEY = urandom(12)

# TODO fail if missing
PLANT_JAR = environ.get("PLANT_JAR", "/opt/plantuml.jar")
logging.info(f"Using {PLANT_JAR}")

WILL_BRAND = environ.get('WILL_BRAND', False)

#
# 3rd party
#
GA_ID = environ.get("GA_ID")
GITHUB_TOKEN = 'github_token'
GITHUB_CLIENT_ID = environ['GITHUB_CLIENT_ID']
GITHUB_SECRET = environ['GITHUB_SECRET']
GITHUB_STATE = str(uuid.uuid4()) # unique for each user
# authenticated users get 100x more requests
# TODO: if bath auth, does it fail?
DEFAULT_USER = 'pointillismio'

PAYPAL_CLIENT_ID = environ.get('PAYPAL_CLIENT_ID')
