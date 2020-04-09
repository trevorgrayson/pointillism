from os import environ

from config import LDAP_HOST, LDAP_BASE_DN, ADMIN_USER, ADMIN_PASS
from ldapauth import LdapAuth

    
if __name__ == '__main__':
    client = LdapAuth(LDAP_HOST, LDAP_BASE_DN, ADMIN_USER, ADMIN_PASS)
    # print(create(environ['USER'], environ['PASS']))

    result = client.authenticate(environ['USER'], environ['PASS'])
    print(result)
    
