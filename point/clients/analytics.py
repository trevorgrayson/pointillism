import logging
from config import GA_ID
from urllib import parse
from http.client import HTTPSConnection
HOST = 'www.google-analytics.com'


class GAnalytics:
    def __init__(self):
        if GA_ID is None:
            logging.warning("GA_ID is not set.  Analytics will not be reported.")
        else:
            self.client = HTTPSConnection(HOST)

    def pageview(self, path, user_id=None, **params):
        if GA_ID is None:
            return

        self.client.request("GET", self.url(path=path,
                                            user_id=user_id))

    def url(self, path=None, user_id=None, **params):
        """
        # tid=UA-xxxxxxxxxx-2
        # t=event
        # ec=testCategory
        # ea=testAction
        # v=1
        # cid=12345678
        """
        p = (
            "t=pageview",
            "v=1",
            "ec=services",
            "ea=render",
            f"dp={parse.quote(path)}"  # page path
        )
        if user_id is not None:
            p += (f'cid={user_id}',)

        if GA_ID is not None:
            p += (f"tid={GA_ID}",)

        return "/collect?" + \
               "&".join(p)
