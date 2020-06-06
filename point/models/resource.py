class GitResource:
    def __init__(self, owner, project, branch, path):
        self.owner = owner
        self.project = project
        self.branch = branch
        self.path = path

    def split(self):
        return self.path.split('/')

    def __str__(self):
        return f'https://github.com/{self.owner}/{self.project}/blob/{self.branch}/{self.path}'

    @classmethod
    def parse(cls, url):
        protocol, _, domain, owner, project, *rest = url.split("/")
        return GitResource(
            owner, project, None, "/".join(rest)
        )
