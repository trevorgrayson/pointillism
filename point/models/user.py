import uuid
from point.models.base import LDIFRecord
from .domain.user import (
    User, GIT_TOKEN, PT_SESSION_TOKEN, FILTER_FIELDS, BALANCE
)


class GitHubUser(LDIFRecord):
    type = 'cn'
    attributes = ['sn', 'cn', 'description', GIT_TOKEN, PT_SESSION_TOKEN, BALANCE]

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
        if response:
            return next(iter([User(**args) for args in response]))
        else:
            return []

    @classmethod
    def find(cls, **attributes):
        base_dn = 'dc=ipsumllc,dc=com' # cls.base_dn
        # if 'base_dn' in attributes:
        #     base_dn = ','.join((attributes['base_dn'], base_dn))
        #     del attributes['base_dn']
        filters = []

        for field in FILTER_FIELDS:
            if field in attributes.keys():
                if field == 'token':
                    filters.append(f'({GIT_TOKEN}={attributes[field]})')
                elif field == 'email':
                    filters.append(f'(Email={attributes[field]})')
                else:
                    filters.append(f'({field}={attributes[field]})')

        search_filter = ''.join(filters)
        if len(filters) > 1:
            search_filter = f'(&{search_filter})'
        # f'(&(objectClass={cls.type_name()})({search}))'
        response = cls._search(base_dn, search_filter, **attributes)
        return list([User(**args) for args in response])

    def pays(self, amount):
        for user in self.users:
            raise NotImplementedError("Need to update user")
            user.balance += amount
            self.update(user)
