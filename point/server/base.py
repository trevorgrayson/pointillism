import logging
from functools import wraps
from flask import redirect, request, make_response
from point.models import GitHubUser

LOG = logging.getLogger(__name__)


def get_me():
    token = request.cookies.get("github_token")

    if token is not None:
        user = GitHubUser.search_token(token)

        if user:
            return user[0]

def login_required(fn):
    """ flask endpoint wrapper. if logged in continue, else redirect to login """
    @wraps(fn)
    def wrapped(*args, **kwargs):
        token = request.cookies.get("github_token")
        if token:
            return fn(*args, **kwargs)
        else:
            return make_response(redirect('/github/login'))

    return wrapped
