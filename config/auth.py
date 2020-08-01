from os import environ


LDAP_HOST = environ.get('LDAP_HOST')
# TODO 'ldap://openldap') ldap://users-service
LDAP_BASE_DN = environ.get('BASE_DN', "dc=ipsumllc,dc=com")

ADMIN_USER = environ.get('ADMIN_USER')
ADMIN_PASS = environ.get('ADMIN_PASS')


def using_ldap():
    return LDAP_HOST is not None


