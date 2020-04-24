"""
Users can add to a running balance.
At the beginning of each month, FEE_PER_MONTH will be decremented [IF subscribed].

TODO: Need a monthly process.
"""
from point.models import GitHubUser


def credit(user, amt):
    user.pays(amt)
    GitHubUser(user).pays()
