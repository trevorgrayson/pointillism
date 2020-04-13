from flask import Blueprint, redirect, request, make_response
from config import DOMAIN, HOST, ENV, STATIC_DIR, PAYPAL_CLIENT_ID
from config import GITHUB_TOKEN, GITHUB_CLIENT_ID, GITHUB_SECRET, GITHUB_STATE
from string import Template
from ldapauth import LdapAuth
from config import LDAP_HOST, ADMIN_USER, ADMIN_PASS
from server.base import login_required, get_me
from models.base import GitHubRepo

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
    response = make_response(redirect('/github'))
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
