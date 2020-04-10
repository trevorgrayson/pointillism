import logging
from ldap3 import (
    Server, Connection, core, extend, HASHED_SALTED_SHA,
    MODIFY_REPLACE, MODIFY_ADD
)
from ldap3.utils.hashed import hashed
from ldap3.core.exceptions import LDAPChangeError

from config import ADMIN_PASS
from .models import User
from .utils import cn_for, nsplit
from .client import LdapAuth, NotVerified

LOG = logging.getLogger(__name__)

