from models.base import LDIFRecord


class GitHubRepo(LDIFRecord):
    type = 'ou'
    attributes = ['ou', 'description']

    @classmethod
    def search_repo(cls, org, name, **attributes):
        # base_dn = f'ou={org},cn={user},dc=ipsumllc,dc=com' # cls.base_dn
        base_dn = f'dc=ipsumllc,dc=com'
        search_filter = f'(ou={name})'

        response =  cls._search(base_dn, search_filter, **attributes)
        return list([Repo(**args) for args in response])


class Repo:
    def __init__(self, **record):
        attrs = record.get('attributes', {})
        self.name = next(iter(attrs.get('ou')), None)
        self.dn = attrs.get('dn')

    @property
    def credentials(self):
        pass
