#
# server.auth
#
from flask import Blueprint, redirect, request, make_response, g, session
from werkzeug.wrappers import Response

from ldapauth import LdapAuth
from ldapauth.utils import InvalidLDAPUser
from ldapauth import NotVerified
from config import LDAP_HOST, LDAP_BASE_DN, ADMIN_USER

USER_MAP = {
    'admin': 'tg'
}


try:
    CLIENT = LdapAuth(LDAP_HOST, LDAP_BASE_DN, ADMIN_USER)
except InvalidLDAPUser:
    raise Exception(f"ADMIN_USER '{ADMIN_USER}' is malformed. Please update the ADMIN_USER env variable")


def register_config(app, **config):
    app.config['LDAP_HOST'] = config['ldap_host']
    app.config['LDAP_BASE_DN'] = config['ldap_base_dn']
    app.config['LDAP_USERNAME'] = config['ldap_username']
    app.config['LDAP_PASSWORD'] = config['ldap_password']
    app.config['LDAP_LOGIN_VIEW'] = config['ldap_login_view']


auth_routes = Blueprint('auth', __name__)

@auth_routes.route("/login", methods=['post'])
def login():
    if g.user:
        return make_response(redirect(
            '/' + USER_MAP.get(user.name, user.name), 
            code=302
        ))

    username = request.form["username"]
    password = request.form["password"]

    try:
        user = CLIENT.authenticate(username, password)
    except NotVerified:
        return "forbidden", 403
      

    if not user:
        return redirect('/', code=302)

    session['username'] = user.name
    resp = make_response(redirect(
        '/' + USER_MAP.get(user.name, user.name), 
        code=302
    ))
    return resp
