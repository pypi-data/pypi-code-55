#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.common import dt_heading

import my.rss as mr


class RssSubscriptions(StaticView):
    def get_items(self):
        for s in mr.get_all_subscriptions():
            yield node(
                link(url=s.url, title=s.title) + ('' if s.subscribed else ' UNSUBSCRIBED'),
            )


if __name__ == '__main__':
    RssSubscriptions.main()
