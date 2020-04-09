class InvalidLDAPUser(Exception): pass


def nsplit(email):
    """email to cn, domain to dn
    
    >>> nsplit('admin@whatever.com')
    'cn=admin,dc=whatever,dc=com'

    >>> nsplit("whatever.com")
    'dc=whatever,dc=com'
    """
    try:
        pair = email.split('@')
        tail = pair[0]
        out = ''

        if len(pair) > 1:
            user, tail = pair
            out = f"cn={user},"

        out += 'dc='
        doms = tail.split('.')

        return out + ",dc=".join(doms)
    except AttributeError:
        raise InvalidLDAPUser(f"Could not parse `{email}`. Expecting email address format.")


def cn_for(username, dn):
    """
    >>> cn_for('angus', 'dc=phoenixfoundation,dc=org')
    'cn=angus,dc=phoenixfoundation,dc=org'
    """
    return f"cn={username},{dn}"
