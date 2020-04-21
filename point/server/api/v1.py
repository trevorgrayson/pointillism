from json import dumps as fmt
from flask import Blueprint, request

from point.server.base import get_me
from point.models import GitHubRepo

v1_routes = Blueprint('api_v1', __name__)


@v1_routes.route('/repos', methods=['post'])
def create():
    me = get_me()
    repo = request.form.get('repo')
    if repo:
        repo = repo.split('/')
    else:
        raise Exception("github `repo` variable required.")

    base_dn = GitHubRepo.create(*repo, base_dn=f'cn={me.cn}')
    if base_dn:
        return fmt({"message": "OK"})


@v1_routes.route('/repos', methods=['get'])
def index():
    me = get_me()
    if me:
        repos = GitHubRepo.of(me.name)
        return fmt(list(map(lambda r: r.as_json, repos)))
    else:
        return fmt({'message': 'unavailable'}), 401
