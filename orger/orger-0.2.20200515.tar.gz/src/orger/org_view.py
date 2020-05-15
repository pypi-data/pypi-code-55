#!/usr/bin/env python3
import argparse
from argparse import ArgumentParser, Namespace
import logging
import inspect
from pathlib import Path
from subprocess import check_call
from tempfile import TemporaryDirectory
from typing import List, Tuple, Iterable, Optional

from .inorganic import OrgNode, TimestampStyle
from .state import JsonState
from .atomic_append import PathIsh, atomic_append_check, assert_not_edited
from .common import setup_logger

# TODO tests for determinism? not sure where should they be...
# think of some generic thing to test that?

Key = str
OrgWithKey = Tuple[Key, OrgNode]


_style_map = {
    k.lower(): v
    for k, v in TimestampStyle._member_map_.items() # type: ignore[attr-defined]
}

class OrgView:
    logger_tag: Optional[str] = None
    DEFAULT_HEADER: str = '# should be overridden'

    # TODO cmdline args shouldn't be none?
    def __init__(
            self,
            cmdline_args: Optional[Namespace]=None,
            file_header: Optional[str]=None,
    ) -> None:
        self.cmdline_args: Namespace = cmdline_args if cmdline_args is not None else Namespace()
        tag = self.name() if self.logger_tag is None else self.logger_tag
        self.logger = logging.getLogger(tag)

        tool = Path(inspect.getfile(self.__class__)).absolute()
        self.file_header = file_header if file_header is not None else self.DEFAULT_HEADER.format(tool=tool)

    @property
    def args(self) -> Namespace:
        # TODO deprecate cmdline_args?
        return self.cmdline_args

    @classmethod
    def name(cls):
        return cls.__name__

    def get_items(self) -> Iterable:
        raise NotImplementedError

    def main_common(self) -> None:
        timestamp_style = self.args.timestamps
        from .common import settings
        # hacky, but does the trick for now...
        settings.DEFAULT_TIMESTAMP_STYLE = _style_map[timestamp_style]
        setup_logger(self.logger, level=logging.DEBUG)

    @classmethod
    def parser(cls) -> ArgumentParser:
        p = ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        p.add_argument(
            '--timestamps',
            type=str,
            choices=list(_style_map.keys()),
            default='inactive',
            help="timestamp style, default '%(default)s'",
        )
        return p


# TODO wonder if I could reuse append bits here?
class Mirror(OrgView):
    """
    *Mirror* (old name =StaticView=): mirrors *all data* from a source, and generated from scratch every time, hence *read only*.
    """

    DEFAULT_HEADER = '''
# This file is AUTOGENERATED by {tool}
# It's deliberately read-only, because it will be overwritten next time Orger is run.
# If you want to edit it anyway, you can use chmod +w in your terminal, or M-x toggle-read-only in Emacs.
'''.lstrip()


    @classmethod
    def main(cls, setup_parser=None) -> None:
        p = cls.parser()
        p.add_argument('--to', type=Path, default=Path(cls.name() + '.org'))
        if setup_parser is not None:
            setup_parser(p)

        args = p.parse_args()
        inst = cls(cmdline_args=args)
        inst.main_common()
        inst._run(to=args.to)

    def get_items(self) -> Iterable:
        raise NotImplementedError

    def _run(self, to: Path):
        org_tree = self.make_tree()
        rtree = org_tree.render(level=0)

        assert_not_edited(to)
        # again, not properly atomic, but hopefully enough
        # TODO create a github issue, maybe someone comes up with proper way of solving this
        to.touch()
        check_call(['chmod', '+w', to])
        to.write_text(rtree)
        check_call(['chmod', '-w', to])


    def make_tree(self) -> OrgNode:
        items: List[OrgNode] = []
        for p in self.get_items():
            # it's ok to use items without keys in View
            if isinstance(p, OrgNode):
                items.append(p)
            else:
                items.append(p[1]) # presumably, OrgWithKey

        split = self.file_header.splitlines(keepends=True)
        heading = split[0].rstrip()
        body = ''.join(split[1:])
        return OrgNode(
            # TODO shit. are newlines sanitized from file header??
            heading=heading,
            body=body,
            children=items,
            escaped=True,
        )

    @classmethod
    def make_test(cls, *, heading: str, contains: Optional[str]=None):
        from .inorganic import _from_lazy
        def pick_heading(root: OrgNode, text: str) -> Optional[OrgNode]:
            if text in _from_lazy(root.heading):
                return root
            for ch in root.children:
                chr = pick_heading(ch, text)
                if chr is not None:
                    return chr
            else:
                return None

        def test():
            tree = cls().make_tree() # TODO make sure it works on both static and interactive?
            ll = pick_heading(tree, heading)
            assert ll is not None
            if contains is not None:
                assert contains in ll.render()
        return test
StaticView = Mirror


class Queue(OrgView):
    """
    *Queue* (old name =InteractiveView=): works as a queue, *only previously unseen items* from the data source are appended to the output org-mode file.

    To keep track of old/new items, it's using a separate JSON =state= file.

    A typical usecase is a todo list, or a content processing queue.
    You can use such a module as you use any other org-mode file: schedule/refile/comment/set priorities, etc.
    """

    DEFAULT_HEADER = '''
# This file is AUTOGENERATED by {tool}
'''.lstrip()

    def _run(
            self,
            to: Path,
            state_path: Path,
            init: bool=False,
            dry_run: bool=False,
    ) -> None:
        if not to.exists() and not init:
            raise RuntimeError(f"target {to} doesn't exist! Try running with --init")

        state = JsonState(
            path=state_path,
            logger=self.logger,
            dry_run=dry_run,
        )
        items = list(self.get_items())

        from collections import Counter
        dups = [k for k, cnt in Counter(i[0] for i in items).items() if cnt > 1]
        if len(dups) > 0:
            raise RuntimeError(f'Duplicate items {dups}')

        if not to.exists():
            self.logger.warning("target %s didn't exist, initializing!", to)
            atomic_append_check(to, self.file_header + '\n')

        for key, item in items:
            def action(item=item):
                # not sure about this newline, but better to have extra whitespace than rely on trailing
                rendered = '\n' + item.render(level=1)
                atomic_append_check(
                    to,
                    rendered,
                )
            self.logger.debug('processing %s', key)
            state.feed(
                key=key,
                value=item, # TODO not sure about this one... perhaps only link?
                action=action,
            )

    def get_items(self) -> Iterable[OrgWithKey]:
        raise NotImplementedError

    @classmethod
    def main(cls, setup_parser=None) -> None:
        p = cls.parser()
        p.add_argument('--to'   , type=Path, default=Path(cls.name() + '.org')       , help='file where new items are appended')
        p.add_argument('--state', type=Path, default=Path(cls.name() + '.state.json'), help='state file for keeping track of handled items')
        p.add_argument('--init', action='store_true')
        p.add_argument('--dry-run', action='store_true')
        if setup_parser is not None:
            setup_parser(p)

        args = p.parse_args()
        inst = cls(cmdline_args=args)
        inst.main_common()
        inst._run(
            to=args.to,
            state_path=args.state,
            init=args.init,
            dry_run=args.dry_run,
        )
InteractiveView = Queue


def test_org_view_overwrite(tmp_path: Path):
    class TestView(StaticView):
        def __init__(self, items: List[OrgWithKey], *args, **kwargs) -> None:
            super().__init__(*args, file_header='# autogenerated!\n#+TITLE: sometitle\nalso text\n', **kwargs) # type: ignore
            self.items = items

        def get_items(self):
            return self.items

    rpath = tmp_path / 'test.org'

    TestView([])._run(to=rpath)
    assert rpath.read_text() == '''
# autogenerated!
#+TITLE: sometitle
also text
'''.lstrip()

    TestView([
        # TODO shit, it's gonna use implicit date??
        ('first' , OrgNode(heading='whatever')),
        ('second', OrgNode(heading='alala')), # TODO why was that even necessary??
    ])._run(to=rpath)
    # TODO eh, perhaps use trailing space?
    assert rpath.read_text() == """
# autogenerated!
#+TITLE: sometitle
also text

* whatever
* alala""".lstrip()


def test_org_view_append(tmp_path: Path):
    import json
    class TestView(InteractiveView):
        def __init__(self, items: List[OrgWithKey], *args, **kwargs) -> None:
            super().__init__(*args, file_header='# autogenerated!', **kwargs) # type: ignore
            self.items = items

        def get_items(self):
            for i in self.items:
                yield i

    rpath = tmp_path / 'res.org'
    spath = tmp_path / 'state.json'

    def run_view(items, **kwargs):
        TestView(items)._run(
            to=rpath,
            state_path=spath,
            **kwargs,
        )

    def get_state():
        return set(json.loads(spath.read_text()).keys())

    items = []
    run_view([], init=True)
    assert rpath.read_text() == """
# autogenerated!
""".lstrip()
    # TODO do we need to touch state too??

    items.append(
        ('first', OrgNode(heading='i am first')),
    )
    run_view(items)
    assert rpath.read_text() == """
# autogenerated!

* i am first""".lstrip()
    assert get_state() == {'first'}


    items.append(
        ('second', OrgNode('i am second')),
    )
    run_view(items)
    assert rpath.read_text() == """
# autogenerated!

* i am first
* i am second""".lstrip()
    assert get_state() == {'first', 'second'}


    rpath_time = rpath.stat().st_mtime
    spath_time = spath.stat().st_mtime
    run_view(items)
    assert rpath.stat().st_mtime == rpath_time
    assert spath.stat().st_mtime == spath_time

