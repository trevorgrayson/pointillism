from models.base import LDIFRecord


class GitHubRepo(LDIFRecord):
    type = 'ou'
    attributes = ['ou', 'description']

    @classmethod
    def search_repo(cls, org, name, **attributes):
        # base_dn = f'ou={org},cn={user},dc=ipsumllc,dc=com' # cls.base_dn
        base_dn = f'dc=ipsumllc,dc=com'
        search_filter = f'(ou={name})'

        response = cls._search(base_dn, search_filter, **attributes)
        return list([Repo(**args) for args in response])

    @classmethod
    def first_repo(cls, org, name, **attributes):
        repo = cls.search_repo(org, name, **attributes)
        if repo:
            return repo[0]


class Repo:
    def __init__(self, **record):
        attrs = record.get('attributes', {})
        self.name = next(iter(attrs.get('ou')), None)
        self.dn = record.get('dn')

    @property
    def owner(self):
        if self.dn:
            _, owner, *tail = self.dn.split('cn=')
            owner = owner.split(',')[0]
            return owner

    @property
    def has_owner(self):
        return self.owner is not None
