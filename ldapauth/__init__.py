import logging
from ldap3 import Server, Connection, core, extend, MODIFY_REPLACE, HASHED_SALTED_SHA
from ldap3.utils.hashed import hashed

from config import ADMIN_PASS, LDAP_HOST, LDAP_BASE_DN, ADMIN_USER
from ldapauth.utils import InvalidLDAPUser
from ldapauth.client import LdapAuth

LOG = logging.getLogger(__name__)

class NotVerified(Exception): pass


def cli(args):
    try:
        client = LdapAuth(LDAP_HOST, LDAP_BASE_DN, ADMIN_USER, admin_pass=ADMIN_PASS)
    except InvalidLDAPUser:
        raise Exception(f"ADMIN_USER '{ADMIN_USER}' is malformed. Please update the ADMIN_USER env variable")

    if args.action == 'create':
        password = input("Password for {}:".format(args.username))
        print(client.create(args.username, password))
    else:
        results = client.search(username=args.username)
        print("fetching {}".format(args.username))
        print(results[0])
