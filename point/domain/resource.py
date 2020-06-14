class GitResource:
    def __init__(self, owner=None, project=None, branch=None, path=None):
        self.owner = owner
        self.project = project
        self.branch = branch
        self.path = path

    @classmethod
    def parse(cls, url):
        protocol, _, domain, owner, project, *rest = url.split("/")
        return GitResource(
            owner, project, None, "/".join(rest)
        )
    
    def __str__(self):
        return f'https://github.com/{self.owner}/{self.project}/blob/{self.branch}/{self.path}'
