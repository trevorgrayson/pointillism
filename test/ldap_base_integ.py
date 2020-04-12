from models.base import LDIFRecord

from config import LDAP_BASE_DN


class GitHubRepo(LDIFRecord):
    type = 'ou'
    base_dn = 'dc=github,' + LDAP_BASE_DN
    attributes = ['ou', 'description']


class TestLDIFRecord:
    def test_create(self):
        results = GitHubRepo.create('trevorgrayson', 'private3')

        assert results == True

    def test_search(self):
        results = GitHubRepo.search('private3')

        print(results)

