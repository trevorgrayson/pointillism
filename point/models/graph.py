import uuid
from point.models.base import LDIFRecord
from point.domain.repo import REPO_TOKEN, Repo


class GitHubRepo(LDIFRecord):
    type = 'ou'
    attributes = ['ou', 'description', REPO_TOKEN]

    @classmethod
    def create(cls, *node, **attributes):
        eid = attributes.get(REPO_TOKEN, str(uuid.uuid4()))
        attributes[REPO_TOKEN] = eid

        return super(GitHubRepo, cls).create(*node, **attributes)

    @classmethod
    def search_repo(cls, org, name, **attributes):
        # base_dn = f'ou={org},cn={user},dc=ipsumllc,dc=com' # cls.base_dn
        base_dn = 'dc=ipsumllc,dc=com'
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
        search_filter = '(ou=*)'

        response = cls._search(base_dn, search_filter, **attributes)
        response = filter(lambda r: r['dn'].count('ou') == 2, response)
        return list([Repo(**args) for args in response])
