import argparse
from os import environ

from . import cli
from ldapauth import LdapAuth
from config import (
    LDAP_HOST, LDAP_BASE_DN, ADMIN_USER, ADMIN_PASS, LDAP_HOST
)

parser = argparse.ArgumentParser(description="LDAP Administration")
    
parser.add_argument('username',
                    help="username to act on")
parser.add_argument('action', default='get', nargs='*',
                    help="action to do")

parser.add_argument('--host', default=LDAP_HOST,
                    help="hostname to connect to")
# parser.add_argument('--ldap-admin', dest='admin_user',
#                     default=ADMIN_USER,
#                     help="LDAP Admin user")
# parser.add_argument('--ldap-pass', dest='admin_pass',
#                     default=ADMIN_PASS,
#                     help="LDAP Admin password")


if __name__ == '__main__':
    args = parser.parse_args()
    cli(args)
