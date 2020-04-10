import logging
from ldap3 import (
    Server, Connection, core, extend, HASHED_SALTED_SHA,
    MODIFY_REPLACE, MODIFY_ADD
)
from ldap3.utils.hashed import hashed
from ldap3.core.exceptions import LDAPChangeError

from config import ADMIN_PASS
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

    def create(self, username, password):
        new_cn = cn_for(username, self.base_dn)
        conn = self.connect()
        conn.add(new_cn, ['inetOrgPerson'], {'sn': new_cn})
        modify_password(conn, new_cn, password)

        conn.unbind()
        return User(name=username, authentic=None)

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
