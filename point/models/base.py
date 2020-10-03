import logging

import ldapauth
from ldap3 import Server, Connection, core, SUBTREE
# MODIFY_REPLACE, MODIFY_ADD, HASHED_SALTED_SHA

from ldapauth.utils import nsplit
from config import ADMIN_PASS, LDAP_HOST, LDAP_BASE_DN, ADMIN_USER

LOG = logging.getLogger(__name__)

SUCCESS_RESPONSES = ['success', 'entryAlreadyExists']

TYPE_MAP = {
    'ou': 'organizationalUnit',
    'cn': 'inetOrgPerson'
}

CONN = None


def conn():
    global CONN

    if CONN is None:
        admin_name = nsplit(ADMIN_USER)
        CONN = Connection(LDAP_HOST, admin_name, ADMIN_PASS)
        server = Server(LDAP_HOST, use_ssl=False, port=389, connect_timeout=2)

    return CONN


class LDIFRecord:
    base_dn = LDAP_BASE_DN  # 'dc=github,' + LDAP_BASE_DN

    @classmethod
    def type_name(cls):
        return TYPE_MAP[cls.type]

    @classmethod
    def delete(cls, dn):
        """
        Arguments:
        dn - can be a dn str, or LDIFRecord object.
        Returns: True on success. Raises on failure
        """
        # TODO: duck typing?
        if hasattr(dn, 'dn'):
            dn = dn.dn

        conn().bind()
        if conn().delete(dn):
            return True
        else:
            desc = conn().result['description']
            raise Exception(f'Request Exception: {desc}')

    @classmethod
    def create(cls, *node, **attributes):
        dn = cls.base_dn
        if 'base_dn' in attributes:
            dn = ','.join((attributes['base_dn'], dn))
            del attributes['base_dn'] 

        conn().bind()
        desc = None

        for name in node:
            dn = f'{cls.type}={name},{dn}'
            LOG.info(f'CREATING {dn}({cls.type_name()}: {attributes}')
            conn().add(dn, [cls.type_name()], attributes=attributes)

            desc = conn().result['description']
            if desc not in SUCCESS_RESPONSES:
                raise Exception(f'{dn}: {desc} {conn().result}')

        conn().unbind()

        return desc in SUCCESS_RESPONSES

    @classmethod
    def update(cls, user, **attributes):
        return True

    @classmethod
    def _search(cls, base_dn, search_filter, **attributes):
        LOG.debug(f'SEARCHING {base_dn} with: {search_filter}')

        try:
            if not conn().bind():
                LOG.error(conn().result)
                raise Exception(f"Connection Exception: {conn().result}")

            conn().search(base_dn,
                        search_filter=search_filter,
                        search_scope=SUBTREE,
                        attributes=cls.attributes
                        )

            results = conn().result

            # TODO is over matching. confirm tree works
            if results['description'] == 'success':
                LOG.debug(f'SEARCHING FOUND: {len(conn().response)}')
                return conn().response
            else:
                raise Exception(f'SEARCHING: Request Exception: {results}')

        except core.exceptions.LDAPSocketOpenError as err:
            LOG.error(err)
            raise err

    @classmethod
    def write(cls, dn):
        conn().bind()
        conn().add(dn, [cls.type_name()]) # , {'sn': dn})
        desc = conn().result['description']
        if desc != 'success':
            raise Exception(desc + str(conn().result))
        conn().unbind()

        return desc
