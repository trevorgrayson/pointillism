class User:
    def __init__(self, *args, **kwargs):
        """args is expected to be an tuple item from search_s response """
        self.name = kwargs.get('name')
        self.authentic = kwargs.get('authentic', False)

        if len(args) > 0:
            tup = args[0]
            self.name = tup[1]['cn'][0]
            # self.description

    def __str__(self):
        return f"<User {self.name} {self.authentic}>"

