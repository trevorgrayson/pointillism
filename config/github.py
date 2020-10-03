import uuid
from os import environ


GA_ID = environ.get("GA_ID")

# for individual
GITHUB_TOKEN = environ.get("GITHUB_TOKEN")

# for app
GITHUB_CLIENT_ID = environ.get('GITHUB_CLIENT_ID')
GITHUB_SECRET = environ.get('GITHUB_SECRET')
GITHUB_STATE = str(uuid.uuid4())  # unique for each user

# authenticated users get 100x more requests
# TODO: if bath auth, does it fail?
DEFAULT_USER = 'pointillismio'
DEFAULT_TOKEN = environ.get("DEFAULT_TOKEN") # not likely used
