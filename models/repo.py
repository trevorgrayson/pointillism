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

    @classmethod
    def of(cls, username, **attributes):
        """ return repos owned by username """
        base_dn = f'cn={username},dc=ipsumllc,dc=com'
        search_filter = f'(ou=*)'

        response = cls._search(base_dn, search_filter, **attributes)
        response = filter(lambda r: r['dn'].count('ou') == 2, response)
        return list([Repo(**args) for args in response])


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

    @property
    def label(self):
        repo, org, *tail = self.dn[2:].split(',')
        repo = repo.split('=')[1]
        org = org.split('=')[1]

        return f"{org}/{repo}"

    @property
    def as_json(self):
        return {
            'name': self.label
        }
