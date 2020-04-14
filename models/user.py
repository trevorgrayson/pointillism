import uuid
from models.base import LDIFRecord

TOKEN = 'employeeNumber'


class GitHubUser(LDIFRecord):
    type = 'cn'
    attributes = ['sn', 'cn', 'description', 'givenName', TOKEN]

    @classmethod
    def create(cls, *node, **attributes):
        eid = attributes.get(TOKEN, str(uuid.uuid4()))
        attributes[TOKEN] = eid

        return super(GitHubUser, cls).create(*node, **attributes)

    @classmethod
    def first(cls, cn, **attributes):
        base_dn = 'dc=ipsumllc,dc=com' # cls.base_dn
        search_filter = f'(cn={cn})'

        response = cls._search(base_dn, search_filter, **attributes)
        return next(iter([User(**args) for args in response]))

    @classmethod
    def search_token(cls, token, **attributes):
        base_dn = 'dc=ipsumllc,dc=com' # cls.base_dn
        # if 'base_dn' in attributes:
        #     base_dn = ','.join((attributes['base_dn'], base_dn))
        #     del attributes['base_dn'] 
        search = f'givenName={token}'
        search_filter = f'(givenName={token})' # f'(&(objectClass={cls.type_name()})({search}))'

        response = cls._search(base_dn, search_filter, **attributes)
        return list([User(**args) for args in response])


class User:
    """
    github token: givenName
    p.io token: employeeNumber
    """
    def __init__(self, **record):
        self.dn = record.get('dn')
        attrs = record.get('attributes', {})
        self.name = next(iter(attrs.get('cn')), None)
        self.cn = next(iter(attrs.get('cn')), None)
        self.git_token = attrs.get('givenName')
        if len(self.git_token) > 0:
            self.git_token = self.git_token[0]
        self.token = attrs.get(TOKEN)

        if self.token:
            self.token = self.token[-1]

    def __str__(self):
        return f'User<{self.name}>'

    def __repr__(self):
        return f'User<{self.name}>'
