from plone import api
from zope.publisher.browser import BrowserView


class NoticeView(BrowserView):

    def get_localized_expiration_date(self):
        return api.portal.get_localized_time(self.context.expires())
