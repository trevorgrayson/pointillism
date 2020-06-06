from point.models.base import LDIFRecord


class Graph:
    def __init__(self, params):
        self.dn = params['dn']

    # TODO sub ou only
    @property
    def is_file(self):
        return self.dn.count('ou=') > 2

    @property
    def url(self):
        tokens = self.dn.split(",")[:-3]
        tokens = map(lambda t: t[3:], tokens)
        tokens = reversed(list(tokens))
        path = "/".join(tokens)
        return f"/{path}"

    @property
    def as_json(self):
        return {
            'url': self.url
        }

class GraphDAO(LDIFRecord):
    type = 'ou'
    attributes = ['ou', 'description']

    @classmethod
    def create(cls, repo, user, *node, **attributes):
        org = repo.owner # wrong?
        node = (org, repo.name, *node)
        return super(GraphDAO, cls).create(*node, base_dn=f'cn={user}')

    @classmethod
    def find(cls, owner, org, name, **attributes):
        # base_dn = f'ou={org},cn={user},dc=ipsumllc,dc=com' # cls.base_dn
        base_dn = f'ou={name},ou={org},cn={owner},dc=ipsumllc,dc=com'
        search_filter = f'(ou=*)'

        response = cls._search(base_dn, search_filter, **attributes)
        graphs = filter(lambda g: g.is_file, map(Graph, response))
        return list(graphs)
