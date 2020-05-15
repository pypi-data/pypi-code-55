#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.common import dt_heading

from my.books.kobo import get_books_with_highlights, Highlight


class KoboView(StaticView):
    def get_items(self):
        def render_highlight(h: Highlight):
            # TODO FIXME could use bookmark page??
            heading = 'bookmark' if h.kind == 'bookmark' else (h.text or '')
            body = h.annotation # TODO check if empty
            return node(
                heading=dt_heading(h.dt, heading),
                body=body,
            )

        for page in get_books_with_highlights():
            yield str(page.book), node(
                heading=dt_heading(page.dt, str(page.book)),
                children=[render_highlight(h) for h in page.highlights],
            )


# TODO maybe fixture instead?
test = KoboView.make_test(
    heading='Unsong',
    contains='Singer',
)


if __name__ == '__main__':
    KoboView.main()
