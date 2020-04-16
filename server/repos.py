from flask import Blueprint, redirect, request, make_response
from config import HOST, STATIC_DIR
from string import Template

from server.base import login_required, get_me
from models import GitHubRepo

GITHUB_BASE_DN = 'dc=ipsumllc,dc=com'
API_HOST = 'https://api.github.com'

repo_routes = Blueprint('repo_routes', __name__)


@repo_routes.route('/repos', methods=['POST'])
# @login_required
def repo_claim():
    """ create repo, under a username """
    me = get_me()
    repo = request.form.get('repo')
    
    if repo:
        repo = repo.split('/')
    else:
        raise Exception("github `repo` variable required.")

    base_dn = GitHubRepo.create(*repo, base_dn=f'cn={me.cn}')
    response = make_response(redirect('/repos'))
    return response


@repo_routes.route('/repos')
@login_required
def new():
    me = get_me()
    with open(STATIC_DIR + '/repo_new.html', 'r') as fp:
        template = Template(fp.read())

        return template.substitute(
            username=me.name,
            host=HOST
        )
