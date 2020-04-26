import logging

from ldap3 import Server, Connection, core, MODIFY_REPLACE, MODIFY_ADD, HASHED_SALTED_SHA, SUBTREE

from ldapauth.utils import cn_for, nsplit
from config import ADMIN_PASS, LDAP_HOST, LDAP_BASE_DN, ADMIN_USER

LOG = logging.getLogger(__name__)
ADMIN_NAME = nsplit(ADMIN_USER)
CONN = Connection(LDAP_HOST, ADMIN_NAME, ADMIN_PASS)
SERVER = Server(LDAP_HOST, use_ssl=False, port=389, connect_timeout=2)

SUCCESS_RESPONSES = ['success', 'entryAlreadyExists']


TYPE_MAP = {
    'ou': 'organizationalUnit',
    'cn': 'inetOrgPerson'
}


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

        CONN.bind()
        if CONN.delete(dn):
            return True
        else:
            desc = CONN.result['description']
            raise Exception(f'Request Exception: {desc}')

    @classmethod
    def create(cls, *node, **attributes):
        dn = cls.base_dn
        if 'base_dn' in attributes:
            dn = ','.join((attributes['base_dn'], dn))
            del attributes['base_dn'] 

        CONN.bind()
        desc = None

        for name in node:
            dn = f'{cls.type}={name},{dn}'
            LOG.info(f'CREATING {dn}({cls.type_name()}: {attributes}')
            CONN.add(dn, [cls.type_name()], attributes=attributes)

            desc = CONN.result['description']
            if desc not in SUCCESS_RESPONSES:
                raise Exception(f'{dn}: {desc} {CONN.result}')

        CONN.unbind() 

        return desc in SUCCESS_RESPONSES

    @classmethod
    def _search(cls, base_dn, search_filter, **attributes):
        LOG.debug(f'SEARCHING {base_dn} with: {search_filter}')

        try:
            if not CONN.bind():
                LOG.error(CONN.result)
                raise Exception(f"Connection Exception: {CONN.result}")

            CONN.search(base_dn,
                        search_filter=search_filter,
                        search_scope=SUBTREE,
                        attributes=cls.attributes
                        )

            results = CONN.result

            # TODO is over matching. confirm tree works
            if results['description'] == 'success':
                LOG.debug(f'RESPONSE: {CONN.response}')
                return CONN.response
            else:
                raise Exception(f'Request Exception: {results}')

        except core.exceptions.LDAPSocketOpenError as err:
            LOG.error(err)
            return False

    @classmethod
    def write(cls, dn):
        CONN.bind()
        CONN.add(dn, [cls.type_name()]) # , {'sn': dn})
        desc = CONN.result['description']
        if desc != 'success':
            raise Exception(desc + str(CONN.result))
        CONN.unbind() 

        return desc
