"""
Info commands.
"""

import sys

from collections import defaultdict

from ditz.config import config as userconfig
from ditz import display

from .utils import ditzcmd


class CmdInfo(object):
    @ditzcmd
    def do_todo(self, args):
        """
        Command:
           todo -- Generate todo list

        Usage:
           todo [RELEASE] [-a]

        Arguments:
           RELEASE        Release to display

        Options:
           -a, --all      Also show closed issues
        """

        show_todo(self, allflag=args.all, release=args.RELEASE)

    @ditzcmd
    def do_show(self, args):
        """
        Command:
           show -- Describe a single issue

        Usage:
           show [ISSUE]

        Arguments:
           ISSUE    Issue tag or ID
        """

        issue, _ = self.getissue(args.ISSUE)
        text = display.show_issue(self.db, issue)
        self.write(text)

    @ditzcmd
    def do_log(self, args):
        """
        Command:
           log -- Show recent activity (long form)

        Usage:
           log [COUNT]

        Arguments:
           COUNT    Number of log lines to show

        Details:
           If no count is given, the value is taken from the 'log_lines'
           configuration value (default: 5).  If a count is given, it
           becomes the new default.  A count of zero means show all log
           entries.
        """

        if not hasattr(self, "last_log"):
            self.config.add('lines', 5)
            self.last_log = self.config.getint('lines')

        count = self.getvalue(args.COUNT, int)

        if count is None:
            count = self.last_log
        else:
            self.last_log = count

        text = display.log_events(self.db, count=count, verbose=True)
        self.write(text)

    @ditzcmd
    def do_shortlog(self, args):
        """
        Command:
           shortlog -- Show recent activity (short form)

        Usage:
           shortlog [COUNT]

        Arguments:
           COUNT    Number of log lines to show

        Details:
           If no count is given, the value is taken from the
           'shortlog_lines' configuration value (default: 20).  If a count
           is given, it becomes the new default.  A count of zero means
           show all log entries.
        """

        if not hasattr(self, "last_shortlog"):
            self.config.add('lines', 20)
            self.last_shortlog = self.config.getint('lines')

        count = self.getvalue(args.COUNT, int)

        if count is None:
            count = self.last_shortlog
        else:
            self.last_shortlog = count

        text = display.log_events(self.db, count=count)
        self.write(text)

    @ditzcmd
    def do_changelog(self, args):
        """
        Command:
           changelog -- Generate a changelog for a release

        Usage:
           changelog RELEASE

        Arguments:
           RELEASE    Release to display
        """

        name = self.getrelease(args.RELEASE)
        text = display.show_changelog(self.db, name)
        self.write(text)

    @ditzcmd
    def do_list(self, args):
        """
        Command:
           list -- List issues

        Usage:
           list [REGEXP...]

        Arguments:
           REGEXP  Only show issues matching this regexp
        """

        regexp = self.getregexp(" ".join(args.REGEXP))
        text = display.show_issues(self.db, regexp=regexp, release=True)
        self.write(text or "No matching issues")

    @ditzcmd
    def do_mine(self, args):
        """
        Command:
           mine -- Show issues claimed by you

        Usage:
           mine [-a]

        Options:
           -a, --all      Also show closed issues
        """

        show_todo(self, allflag=args.all, claimed=True)

    @ditzcmd
    def do_claimed(self, args):
        """
        Command:
           claimed -- Show claimed issues by claimer

        Usage:
           claimed [-a]

        Options:
           -a, --all      Also show closed issues
        """

        claimed = defaultdict(list)
        for issue in self.db.issues:
            if issue.claimer and (args.all or not issue.closed):
                claimed[issue.claimer].append(issue)

        if claimed:
            for claimer, issues in sorted(claimed.items()):
                text = display.show_issues(self.db, issues=issues,
                                           release=True)
                self.write(claimer + ":")
                self.write(text)
        else:
            self.write("No issues")

    @ditzcmd
    def do_unclaimed(self, args):
        """
        Command:
           unclaimed -- Show unclaimed issues

        Usage:
           unclaimed [-a]

        Options:
           -a, --all      Also show closed issues
        """

        issues = self.db.issues
        issues = filter(lambda issue: not issue.claimer, issues)

        if not args.all:
            issues = filter(lambda issue: not issue.closed, issues)

        text = display.show_issues(self.db, issues=issues, release=True)
        self.write(text or "No issues")

    @ditzcmd
    def do_status(self, args):
        """
        Command:
           status -- Show project status

        Usage:
           status [RELEASE...]

        Arguments:
           RELEASE     Release(s) to display
        """

        releases = args.RELEASE if args.RELEASE else [None]

        for name in releases:
            text = display.show_status(self.db, name)
            self.write(text)

    @ditzcmd
    def do_releases(self, args):
        """
        Command:
           releases -- Show releases

        Usage:
           releases
        """

        text = display.show_releases(self.db)
        self.write(text or "No releases")

    @ditzcmd
    def do_config(self, args):
        """
        Command:
           config -- Show configuration settings

        Usage:
           config [SECTION]

        Arguments:
           SECTION     Config section to display
        """

        section = args.SECTION

        if not section:
            userconfig.write(sys.stdout)
        elif userconfig.has_section(section):
            for name in sorted(userconfig.options(section)):
                self.write(name, '=', userconfig.get(section, name))
        else:
            self.error("no config section called '%s'" % section)

    @ditzcmd
    def do_info(self, args):
        """
        Command:
           info -- Show database details

        Usage:
           info
        """

        items = (('project', self.db.project.name),
                 ('path', self.db.path),
                 ('issuedir', self.db.config.issue_dir),
                 ('issues', len(self.db.issues)),
                 ('components', len(self.db.project.components)),
                 ('releases', len(self.db.project.releases)))

        for item in items:
            self.write("%11s: %s" % item)


def show_todo(cmd, allflag=False, claimed=False, release=None):
    release = cmd.getrelease(release)
    text = display.show_todo(cmd.db, relname=release, closed=allflag,
                             claimed=claimed)
    cmd.write(text)
