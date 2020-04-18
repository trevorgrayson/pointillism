from os import environ, path, getcwd, urandom
import uuid

DOMAIN = environ.get('domain', 'pointillism.io')
HOST = environ['HOST']
ENV = environ.get('ENV', "PROD")

STATIC_DIR = getcwd()
THEME_DIR = path.join(STATIC_DIR, "themes")

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

# 3rd party
GITHUB_TOKEN = 'github_token'
GITHUB_CLIENT_ID = environ['GITHUB_CLIENT_ID']
GITHUB_SECRET = environ['GITHUB_SECRET']
GITHUB_STATE = str(uuid.uuid4()) # unique for each user

PAYPAL_CLIENT_ID = environ['PAYPAL_CLIENT_ID']
