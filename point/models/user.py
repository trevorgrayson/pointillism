import uuid
from point.models.base import LDIFRecord

PT_SESSION_TOKEN = 'employeeNumber'
SESSION = 'initials'
GIT_TOKEN = 'givenName'


class GitHubUser(LDIFRecord):
    type = 'cn'
    attributes = ['sn', 'cn', 'description', GIT_TOKEN, PT_SESSION_TOKEN]

    def __init__(self, *users):
        self.users = users

    @classmethod
    def create(cls, *node, **attributes):
        eid = attributes.get(PT_SESSION_TOKEN, str(uuid.uuid4()))
        attributes[PT_SESSION_TOKEN] = eid

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
        search = f'{GIT_TOKEN}={token}'
        search_filter = f'({GIT_TOKEN}={token})' # f'(&(objectClass={cls.type_name()})({search}))'

        response = cls._search(base_dn, search_filter, **attributes)
        return list([User(**args) for args in response])

    def pays(self, amount):
        for user in self.users:
            raise NotImplementedError("Need to update user")
            user.balance += amount
            self.update(user)

class User:
    """
    github token: givenName
    p.io token: employeeNumber
    """
    def __init__(self, **record):
        self.dn = record.get('dn')
        attrs = record.get('attributes', {})
        self.name = next(iter(attrs.get('cn', [])), None)
        self.cn = next(iter(attrs.get('cn', [])), None)
        self.git_token = attrs.get(GIT_TOKEN, [])
        if len(self.git_token) > 0:
            self.git_token = self.git_token[-1]
        else:
            self.git_token = None
        self.token = attrs.get(PT_SESSION_TOKEN)
        if self.token:
            self.token = self.token[-1]
        else:
            self.token = None

    def is_authentic(self, session_token):
        return session_token == self.token

    def __str__(self):
        return f'User<{self.name}>'

    def __repr__(self):
        return f'User<{self.name}>'
