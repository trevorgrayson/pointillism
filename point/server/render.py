from flask import Blueprint, request

from config import using_ldap
import logging as log
from json import dumps
from point.server.base import get_me
from point.models import GitHubRepo, GitHubUser, GitResource, User
from point.clients.gitcontent import GitContent
from point.renderer import render, cache_control
from .utils import parse_request_fmt, parse_request_path, convert
from .exception_handling import notifier
from github import GithubException
from point.clients.analytics import GAnalytics

render_routes = Blueprint('render_routes', __name__)


def is_allowed(repo, token):
    return repo and repo.has_owner and \
           repo.requires_token and \
           repo.token == token


def can(me, repo):
    return me.cn == repo.owner.cn


def is_public(user):
    return user.git_token is None


def get_creds(repo):
    """
    returns a user object
    fully hydrated, or from passed token
    or from default config
    """
    creds = User(git_token=[request.args.get('token')])

    if using_ldap() and is_allowed(repo, request.args.get('token')):
        log.debug(f"Authenticated as {repo.owner}")
        owner = GitHubUser.first(repo.owner)
        creds = owner

    return creds


@render_routes.route('/convert', methods=['post'])
def convert_endpt():
    me = get_me()
    url = request.json.get('url')
    if not url:
        return 401, '{"message": "include url param"}'

    protocol, _, _domain, org, project, *rest = url.split('/')
    protocol = protocol.replace(':', '')
    rest = "/".join(rest)

    creds = None
    repo = GitHubRepo.first(org, project)
    if using_ldap() and repo:
        owner = GitHubUser.first(repo.owner)
        # TODO tests
        if owner.cn == repo.owner and can(me, repo):
            creds = repo.token

    return dumps({
       'url': convert(org, project, rest, creds, protocol=protocol)
    })


@render_routes.route("/<string:org>/<string:project>/blob/<string:branch>/<path:path>")
@render_routes.route("/github/<string:org>/<string:project>/<string:branch>/<path:path>")
@render_routes.route("/<string:org>/<string:project>/<string:branch>/<path:path>")
def render_github_url(org, project, branch, path):
    log.debug("REQUEST /github: {path}")
    user_id = 'anonymous'
    resource = GitResource(org, project, branch, path)
    fmt = parse_request_fmt(path)
    path = parse_request_path(path)
    render_params = {
        "theme": request.args.get('theme'),
        "format": fmt[1:]
    }

    repo = GitHubRepo.first(org, project)
    log.debug(repo)
    creds = get_creds(repo)

    try:
        log.debug(f"fetching {resource}")
        body = GitContent(creds).get(org, project, branch, path)
        resp = render(body, **render_params)
        resp.headers = cache_control(is_public(creds), resp.headers)
        GAnalytics().pageview(resource.analytics_path, user_id)
        return resp
    except GithubException as err:
        log.error(err)
        notifier.notify(Exception(
            f"Graph Not Found: {request.path}"
        ))
        return dumps({
            'message': f"Exception finding document: {resource}. " +
                       'Is the repository private? Do you need a valid token?'
        }), 404
