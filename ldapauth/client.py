import logging
from ldap3 import Server, Connection, core, extend, MODIFY_REPLACE, MODIFY_ADD, HASHED_SALTED_SHA, SUBTREE
from ldap3.utils.hashed import hashed
from ldap3.core.exceptions import LDAPChangeError

from config import ADMIN_PASS, LDAP_HOST, LDAP_BASE_DN, ADMIN_USER
from .models import User
from .utils import cn_for, nsplit

LOG = logging.getLogger(__name__)


class NotVerified(Exception): pass


class LdapAuth:
    def __init__(self, host, base_dn, admin_user, admin_pass=None):
        # TODO to config
        self.server = Server(host, use_ssl=False, port=389, connect_timeout=2)
        self.base_dn = base_dn
        self.admin = nsplit(admin_user)
        self.admin_pass = admin_pass
        self.conn = None

    def authenticate(self, username, password):
        cn_filter = cn_for(username, self.base_dn)

        try:
            LOG.info("Connecting")
            self.conn = Connection(self.server, cn_filter, password)
            LOG.debug(self.conn)
            LOG.info("binding")
            if not self.conn.bind():
                raise NotVerified(f"could not verify user {cn_filter} {self.conn.result}")

            LOG.debug(f"returning {username}")
            return User(name=username, authentic=True)

        except core.exceptions.LDAPSocketOpenError as err:
            LOG.error(err)
            return False

    def connect(self):
        if self.conn:
            return self.conn

        try:
            self.conn = Connection(self.server, self.admin, self.admin_pass)

            if not self.conn.bind():
                LOG.error(self.conn.result)
                return False

            return self.conn
        except core.exceptions.LDAPSocketOpenError as err:
            LOG.error(err)
            return False

    def create(self, username, password=None):
        new_cn = cn_for(username, self.base_dn)
        conn = self.connect()
        conn.add(new_cn, ['inetOrgPerson'], {'sn': new_cn})
        if password is not None:
            modify_password(conn, new_cn, password)

        conn.unbind() # TODO needs to be cleaned up
        return User(name=username, authentic=None)

    def search(self, **params):
        username = params.get('username')
        search = f'cn={username}'
        search_filter = f'(&(objectClass=inetOrgPerson)({search}))'
        LOG.debug(search_filter)

        try:
            conn = Connection(self.server, self.admin, self.admin_pass)

            if not conn.bind():
                LOG.error(conn.result)
                return False

            conn.search(self.base_dn,
                        search_filter=search_filter,
                        attributes = ['cn', 'sn', 'givenName']
                        )

            results = conn.response
            # conn.unbind()
            print(results)
            return list(map(record2user, results))
            # return User(name=username, authentic=None)

        except core.exceptions.LDAPSocketOpenError as err:
            LOG.error(err)
            return False

    def delete(self, user):
        conn = self.connect()
        conn.delete(cn_for(user.name, self.base_dn))

        return conn.result['description'] == 'success'
        
    def update(self, user):
        conn = self.connect()
        changes = {k: [(MODIFY_ADD, [v])] for k, v in user.attributes.items()}

        try:
            conn.modify(cn_for(user.name, self.base_dn), changes) 
        except LDAPChangeError:
            pass

        return user


def record2user(record):
    attrs = record['attributes']
    return User(name=attrs['cn'][0])


def modify_password(conn, user_cn, password):
    hashed_password = hashed(HASHED_SALTED_SHA, password)
    changes = {
        'userPassword': [(MODIFY_REPLACE, [hashed_password])]
    }
    success = conn.modify(user_cn, changes=changes)
    if not success:
        LOG.error('Unable to change password for %s' % user_cn)
        LOG.error(conn.result)
        raise ValueError('Unable to change password')
