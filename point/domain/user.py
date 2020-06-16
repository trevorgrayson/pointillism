PT_SESSION_TOKEN = 'employeeNumber'
SESSION = 'initials'
GIT_TOKEN = 'givenName'
EMAIL = 'Email'
BALANCE = 'Fax'
SUBSCRIBED = 'telexNumber'

FILTER_FIELDS = ['token', EMAIL, 'cn']


class User:
    """
    github token: givenName
    p.io token: employeeNumber
    """
    def __init__(self, **record):
        self.dn = record.get('dn')
        attrs = record.get('attributes', {})
        self.name = next(iter(attrs.get('cn', [])), None)
        self.cn = next(iter(attrs.get('cn', [])), None)
        self.git_token = record.get('git_token', attrs.get(GIT_TOKEN, []))
        if len(self.git_token) > 0:
            self.git_token = self.git_token[-1]
        else:
            self.git_token = None
        self.token = attrs.get(PT_SESSION_TOKEN)
        if self.token:
            self.token = self.token[-1]
        else:
            self.token = None
        self.balance = attrs.get(BALANCE, 0)
        if isinstance(self.balance, list):
            if len(self.balance) > 0:
                self.balance = self.balance[-1]
            else:
                self.balance = 0
        self.email = attrs.get(EMAIL)
        self.subscribed = attrs.get(SUBSCRIBED) == 'true'

    def is_active(self):
        return True

    def is_authentic(self, session_token):
        return session_token == self.token

    def __str__(self):
        return f'User<{self.name}>'

    def __repr__(self):
        return f'User<{self.name}>'
