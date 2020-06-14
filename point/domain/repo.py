REPO_TOKEN = 'street'


class Repo:
    def __init__(self, **record):
        attrs = record.get('attributes', {})
        self.name = next(iter(attrs.get('ou', [])), None)
        self.token = attrs.get(REPO_TOKEN)
        if self.token:
            self.token = self.token[-1]
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
            'token': self.token
        }

    def __str__(self):
        return f'<Repo {self.owner}/{self.name} {self.token[:5]}>'

    def __repr__(self):
        return self.__str__()
