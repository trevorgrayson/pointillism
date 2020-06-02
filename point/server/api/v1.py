from json import dumps as fmt
from flask import Blueprint, request

from point.server.base import get_me
from point.models import GitHubRepo
from point.clients.gitcontent import GitContent

v1_routes = Blueprint('api_v1', __name__)


@v1_routes.route('/repos', methods=['post'])
def create():
    me = get_me()
    content_client = GitContent(me)
    repo = request.form.get('repo')
    dry_run = request.form.get("dry_run") == "true"
    if repo:
        repo = repo.split('/')
    else:
        raise Exception("github `repo` variable required.")

    owner = content_client.owner(repo[0], repo[1])
    if not owner:
        return fmt({"message": "not found"}), 404

    if not dry_run:
        base_dn = GitHubRepo.create(*repo, base_dn=f'cn={me.cn}')
        if base_dn:
            return fmt({"message": "OK"})
    else:
        return {"owner": owner}, 4

@v1_routes.route('/repos', methods=['get'])
def index():
    me = get_me()
    if me:
        repos = GitHubRepo.of(me.name)
        return fmt(list(map(lambda r: r.as_json, repos)))
    else:
        return fmt({'message': 'unavailable'}), 401

@v1_routes.route('/repos/<string:owner>/<string:repo>', methods=['DELETE'])
def repo_delete(owner, repo):
    me = get_me()

    repo = GitHubRepo.first(owner, repo)
    if repo.owner == me.name:
        GitHubRepo.delete(repo.dn)  # raises
        return '{"message": "OK"}'
    else:
        return '{"message": "unauthorized"}', 401