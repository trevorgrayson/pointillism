from pytest import fixture
from point.models.user import User

TOKEN = 'token123'


class TestUser:
    @fixture
    def record(self):
        return {
            'raw_dn': b'cn=trevorgrayson,dc=ipsumllc,dc=com',
            'dn': 'cn=trevorgrayson,dc=ipsumllc,dc=com',
            'raw_attributes': {
                'sn': [b'cn=trevorgrayson,dc=ipsumllc,dc=com'],
                'cn': [b'trevorgrayson'],
                'givenName': [b'36b61538e7409e3cb11cdd12fa0b5341e1effc70'], 'description': [], 'employeeNumber': []
            },
            'attributes': {
                'sn': ['cn=trevorgrayson,dc=ipsumllc,dc=com'],
                'cn': ['trevorgrayson'],
                'givenName': ['36b61538e7409e3cb11cdd12fa0b5341e1effc70'],
                'description': [], 'employeeNumber': [TOKEN]
            }, 'type': 'searchResEntry'
        }

    @fixture
    def user(self, record):
        return User(**record)

    @fixture
    def user_empty(self):
        return User()

    def test_init(self, user):
        assert isinstance(user, User)
        assert user.cn == 'trevorgrayson'
        assert user.name == 'trevorgrayson'
        assert user.git_token == '36b61538e7409e3cb11cdd12fa0b5341e1effc70'
        assert user.token == TOKEN

    def test_is_authentic(self, user):
        assert user.is_authentic(TOKEN)
        assert user.is_authentic('NOPE') is False

    def test_str(self, user):
        assert str(user) == 'User<trevorgrayson>'

    def test_repr(self, user):
        assert repr(user) == 'User<trevorgrayson>'

    def test_user_empty(self, user_empty):
        assert user_empty.git_token is None
        assert user_empty.token is None
