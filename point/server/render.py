from flask import Blueprint, request

import logging as log
from json import dumps
from point.models import GitHubRepo, GitHubUser, GitResource
from point.clients.gitcontent import GitContent
from point.renderer import render, cache_control
from .utils import parse_request_fmt, parse_request_path
from .errors import notifier
from github import GithubException

render_routes = Blueprint('render_routes', __name__)

@render_routes.route("/<string:org>/<string:project>/blob/<string:branch>/<path:path>")
@render_routes.route("/github/<string:org>/<string:project>/<string:branch>/<path:path>")
@render_routes.route("/<string:org>/<string:project>/<string:branch>/<path:path>")
def render_github_url(org, project, branch, path):
    log.debug("REQUEST /github: {path}")
    resource = GitResource(org, project, branch, path)
    fmt = parse_request_fmt(path)
    path = parse_request_path(path)
    public = True
    creds = request.args.get('token')
    render_params = {
        "theme": request.args.get('theme'),
        "format": fmt[1:]
    }

    repo = GitHubRepo.first_repo(org, project)

    def is_allowed(repo, token):
        return repo and repo.has_owner and \
               repo.requires_token and \
               repo.token == token

    if is_allowed(repo, request.args.get('token')):
        log.debug(f"Authenticated as {repo.owner}")
        owner = GitHubUser.first(repo.owner)
        creds = owner
        public = False
    log.debug(repo)

    try:
        log.debug(f"fetching {resource}")
        body = GitContent(creds).get(org, project, branch, path)
        resp = render(body, **render_params)
        resp.headers = cache_control(public, resp.headers)
        return resp
    except GithubException as err:
        log.error(err)
        notifier.notify(err)
        return dumps({
            'message': f"Exception finding document: {resource}. " + \
                       'Is the repository private? Do you need a valid token?'
        }), 404
