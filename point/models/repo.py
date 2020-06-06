import uuid
from point.models.base import LDIFRecord
from point.models.graph import GraphDAO

REPO_TOKEN = 'street'


class GitHubRepo(LDIFRecord):
    type = 'ou'
    attributes = ['ou', 'description', REPO_TOKEN]

    @classmethod
    def create(cls, *node, **attributes):
        eid = attributes.get(REPO_TOKEN, str(uuid.uuid4()))
        attributes[REPO_TOKEN] = eid

        return super(GitHubRepo, cls).create(*node, **attributes)

    @classmethod
    def search(cls, org, name, **attributes):
        # base_dn = f'ou={org},cn={user},dc=ipsumllc,dc=com' # cls.base_dn
        base_dn = f'dc=ipsumllc,dc=com'
        search_filter = f'(ou={name})'

        response = cls._search(base_dn, search_filter, **attributes)
        return list([Repo(**args) for args in response])

    @classmethod
    def first(cls, org, name, **attributes):
        repo = cls.search(org, name, **attributes)
        if repo:
            return repo[0]

    @classmethod
    def of(cls, username, **attributes):
        """ return repos owned by username """
        base_dn = f'cn={username},dc=ipsumllc,dc=com'
        search_filter = f'(ou=*)'

        response = cls._search(base_dn, search_filter, **attributes)
        response = filter(lambda r: r['dn'].count('ou') == 2, response)
        repos = list([Repo(**args) for args in response])
        for repo in repos:
            try:
                repo.graphs = GraphDAO.find(username, repo.owner, repo.name)
            except Exception:
                pass

        return repos


class Repo:
    def __init__(self, **record):
        attrs = record.get('attributes', {})
        self.name = next(iter(attrs.get('ou', [])), None)
        self.token = attrs.get(REPO_TOKEN)
        if self.token:
            self.token = self.token[-1]
        self.dn = record.get('dn')
        self.graphs = []

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
    def requires_token(self):
        return self.token is not None

    @property
    def label(self):
        repo, org, *tail = self.dn[2:].split(',')
        repo = repo.split('=')[1]
        org = org.split('=')[1]

        return f"{org}/{repo}"

    @property
    def as_json(self):
        return {
            'name': self.label,
            'token': self.token,
            'graphs': [graph.as_json for graph in self.graphs]
        }

    def __str__(self):
        return f'<Repo {self.owner}/{self.name} {self.token[:5]}>'

    def __repr__(self):
        return self.__str__()
