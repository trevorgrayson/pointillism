from os import environ, path, getcwd
import uuid

DOMAIN = environ.get('domain', 'pointillism.necessaryeval.com')
HOST = environ['HOST']
ENV = environ.get('ENV', "PROD")

STATIC_DIR = getcwd() 

if not STATIC_DIR or STATIC_DIR == '/':
    STATIC_DIR = '/srv/vhosts/pointillism'
else:
    STATIC_DIR += '/public'

# 3rd party
GITHUB_TOKEN = 'github_token'
GITHUB_CLIENT_ID = environ.get('GITHUB_CLIENT_ID')
GITHUB_SECRET = environ.get('GITHUB_SECRET')
GITHUB_STATE = str(uuid.uuid4()) # unique for each user

PAYPAL_CLIENT_ID = environ.get('PAYPAL_CLIENT_ID')
