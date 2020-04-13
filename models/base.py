import logging
from ldap3 import Reader
from ldap3 import Server, Connection, core, extend, MODIFY_REPLACE, MODIFY_ADD, HASHED_SALTED_SHA, SUBTREE
from ldap3.utils.hashed import hashed

from ldap3 import ObjectDef, AttrDef, Reader, Writer, Entry, Attribute, OperationalAttribute

from ldapauth.utils import cn_for, nsplit
from config import ADMIN_PASS, LDAP_HOST, LDAP_BASE_DN, ADMIN_USER

LOG = logging.getLogger(__name__)
ADMIN_NAME = nsplit(ADMIN_USER)
CONN = Connection(LDAP_HOST, ADMIN_NAME, ADMIN_PASS)
SERVER = Server(LDAP_HOST, use_ssl=False, port=389, connect_timeout=2)

SUCCESS_RESPONSES = ['success', 'entryAlreadyExists']

def repo_dn(base, vendor, username, org, repo):
    return f'ou={repo},ou={org},ou={username},dc={vendor},{base}'

TYPE_MAP = {
    'ou': 'organizationalUnit',
    'cn': 'inetOrgPerson'
}


class LDIFRecord:
    @classmethod
    def type_name(cls):
        return TYPE_MAP[cls.type]

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
            CONN.add(dn, [cls.type_name()], attributes=attributes)

            desc = CONN.result['description']


            if desc not in SUCCESS_RESPONSES:
                raise Exception(f'{dn}: {desc} {CONN.result}')

        CONN.unbind() 

        return desc in SUCCESS_RESPONSES

    @classmethod
    def search_token(cls, token, **attributes):
        base_dn = 'dc=ipsumllc,dc=com' # cls.base_dn
        # if 'base_dn' in attributes:
        #     base_dn = ','.join((attributes['base_dn'], base_dn))
        #     del attributes['base_dn'] 
        search = f'givenName={token}'
        search_filter = f'(givenName={token})' # f'(&(objectClass={cls.type_name()})({search}))'
        LOG.debug(f'SEARCHING {base_dn} with: {search_filter}')

        response = cls._search(base_dn, search_filter, **attributes)
        return list([User(**args) for args in response])

    @classmethod
    def search_repo(cls, user, org, name, **attributes):
        base_dn = f'ou={org},cn={user},dc=ipsumllc,dc=com' # cls.base_dn
        search_filter = f'(ou={name})'
        LOG.debug(f'SEARCHING {base_dn} with: {search_filter}')

        response =  cls._search(base_dn, search_filter, **attributes)
        return list([Repo(**args) for args in response])

    @classmethod
    def _search(cls, base_dn, search_filter, **attributes):

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


class GitHubRepo(LDIFRecord):
    type = 'ou'
    base_dn = LDAP_BASE_DN  # 'dc=github,' + LDAP_BASE_DN
    attributes = ['ou', 'description']


class User:
    def __init__(self, **record):
        attrs = record.get('attributes', {})
        self.name = next(iter(attrs.get('cn')), None)
        self.cn = next(iter(attrs.get('cn')), None)
        self.dn = attrs.get('dn')
        self.token = next(iter(attrs.get('givenName')), None)

        if self.token:
            self.token = self.token[-1]

    def __str__(self):
        return f'User<{self.name}>'

    def __repr__(self):
        return f'User<{self.name}>'

class Repo:
    def __init__(self, **record):
        attrs = record.get('attributes', {})
        self.name = next(iter(attrs.get('ou')), None)
        self.dn = attrs.get('dn')

    def owner(self):
        pass
    
class GitHubUser(LDIFRecord):
    type = 'cn'
    base_dn = LDAP_BASE_DN  # 'dc=github,' + LDAP_BASE_DN
    attributes = ['sn', 'cn', 'description', 'givenName']
