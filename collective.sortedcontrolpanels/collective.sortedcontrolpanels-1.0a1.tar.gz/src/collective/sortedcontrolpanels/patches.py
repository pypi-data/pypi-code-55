# -*- coding: utf-8 -*-
from Products.CMFCore.Expression import Expression, createExprContext
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from zope.i18n import translate
from zope.i18nmessageid import Message


def enumConfiglets(self, group=None):
    portal = getToolByName(self, 'portal_url').getPortalObject()
    context = createExprContext(self, portal, self)
    res = []
    for a in self.listActions():
        verified = 0
        for permission in a.permissions:
            if _checkPermission(permission, portal):
                verified = 1
        if verified and a.category == group and a.testCondition(context) \
                and a.visible:
            res.append(a.getAction(context))
    # Translate the title for sorting
    if getattr(self, 'REQUEST', None) is not None:
        for a in res:
            title = a['title']
            if not isinstance(title, Message):
                title = Message(title, domain='plone')
            a['title'] = translate(title,
                                   context=self.REQUEST)

    def _title(v):
        return v['title']

    res.sort(key=_title)
    return res
