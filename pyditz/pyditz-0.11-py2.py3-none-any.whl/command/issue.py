"""
Issue commands.
"""

from ditz import flags
from ditz.editor import DitzEditor

from .utils import ditzcmd


class CmdIssue(object):
    @ditzcmd
    def do_add(self, args):
        """
        Command:
           add -- Add a new issue

        Usage:
           add [-b | -t | -f] [-d DESC] [-u USER] [-r RELEASE]
               [-c COMP] [-m COMMENT] [TEXT...]

        Arguments:
           TEXT     Issue title text

        Options:
           -b, --bugfix               Add a bugfix issue
           -t, --task                 Add a task issue
           -f, --feature              Add a feature issue
           -d, --description DESC     Issue description
           -u, --user USER            User reporting the issue
           -r, --release RELEASE      Assign to a release
           -c, --component COMP       Set the component
           -m, --comment COMMENT      Add a comment
        """

        if args.TEXT:
            title = " ".join(args.TEXT)
        else:
            title = self.getline("Title: ", allowempty=False)

        desc = args.description or self.gettext("Description")

        if args.bugfix:
            issuetype = flags.BUGFIX
        elif args.task:
            issuetype = flags.TASK
        elif args.feature:
            issuetype = flags.FEATURE
        else:
            types = {'b': flags.BUGFIX, 'f': flags.FEATURE, 't': flags.TASK}
            while True:
                prompt = "Is this a (b)ugfix, (f)eature or (t)ask? "
                reply = self.getline(prompt)
                if reply and reply[0] in types:
                    issuetype = types[reply[0]]
                    break

        comp = args.component
        if not comp:
            choices = self.db.components
            if len(choices) >= 2:
                comp = self.getchoice("component", choices)
            else:
                comp = None

        release = args.release
        if not release:
            releases = self.db.project.releases
            choices = [r.name for r in releases if not r.released]
            if choices and self.getyesno("Assign to a release now?"):
                if len(choices) > 1:
                    release = self.getchoice("release", choices)
                else:
                    release = choices[0]
                    self.write("Assigning to release", release)

        if args.user:
            reporter = args.user
        else:
            default = self.db.config.username
            prompt = 'Issue creator (enter for "%s"): ' % default
            reporter = self.getline(prompt)

        comment = self.getcomment(args.comment)

        issue = self.db.add_issue(title, desc, type=issuetype,
                                  reporter=reporter, release=release,
                                  component=comp, comment=comment)

        name = self.last_issuename = self.db.issue_name(issue)
        self.write("Added issue", name)

    @ditzcmd
    def do_comment(self, args):
        """
        Command:
           comment -- Comment on an issue

        Usage:
           comment [ISSUE] [-m COMMENT]

        Arguments:
           ISSUE    Issue tag or ID

        Options:
           -m, --comment COMMENT      Comment to add
        """

        issue, name = self.getissue(args.ISSUE)
        self.write("Commenting on %s: %s" % (name, issue.title))

        comment = self.getcomment(args.comment)

        if comment:
            self.db.add_comment(issue, comment)
            self.write("Comments recorded for", name)
        else:
            self.write("Empty comment, aborted")

    @ditzcmd
    def do_edit(self, args):
        """
        Command:
           edit -- Edit an issue

        Usage:
           edit [ISSUE]

        Arguments:
           ISSUE    Issue tag or ID
        """

        issue, name = self.getissue(args.ISSUE)
        self.write("Editing %s: %s" % (name, issue.title))

        path = self.db.issue_filename(issue)
        editor = DitzEditor(path)

        while True:
            text = editor.edit()
            if not editor.error:
                break

            reply = self.getyesno("%s\n\nRe-edit to fix problem?"
                                  % editor.error, True)
            if not reply:
                return

        if editor.modified:
            self.db.edit_issue(issue, text)
            self.write("Updated %s: %s" % (name, issue.title))
        else:
            self.write("No changes made")

    @ditzcmd
    def do_set_component(self, args):
        """
        Command:
           set-component -- Set an issue's component

        Usage:
           set-component [ISSUE] [-c COMP] [-m COMMENT]

        Arguments:
           ISSUE    Issue tag or ID

        Options:
           -c, --component COMP       Set this component
           -m, --comment COMMENT      Add a comment

        Details:
           Other issue tags may change.
        """

        issue, name = self.getissue(args.ISSUE)
        comp = args.component

        self.write("Changing the component of issue %s: %s"
                   % (name, issue.title))

        choices = self.db.components
        if len(choices) < 2:
            self.error("this project does not use multiple components")

        if comp and comp not in choices:
            self.error("unknown component: %s" % comp)

        if not comp:
            if issue.component in choices:
                choices.remove(issue.component)

            comp = self.getchoice("component", choices)

        comment = self.getcomment(args.comment)

        self.db.set_component(issue, comp, comment)
        newname = self.db.issue_name(issue)

        if self.last_issuename == name:
            self.last_issuename = newname

        self.write("Issue %s is now %s.  Other issue names may have changed."
                   % (name, newname))

    @ditzcmd
    def do_add_reference(self, args):
        """
        Command:
           add-reference -- Add a reference to an issue

        Usage:
           add-reference [ISSUE] [-R REF] [-m COMMENT]

        Arguments:
           ISSUE    Issue tag or ID

        Options:
           -R, --reference REF        Reference to add
           -m, --comment COMMENT      Add a comment
        """

        issue, name = self.getissue(args.ISSUE)
        self.write("Adding a reference to %s: %s" % (name, issue.title))

        text = args.reference or self.getline("Reference: ", allowempty=False)
        comment = self.getcomment(args.comment)

        self.db.add_reference(issue, text, comment=comment)
        self.write("Added reference to", name)

    @ditzcmd
    def do_start(self, args):
        """
        Command:
           start -- Start work on an issue

        Usage:
           start [ISSUE] [-m COMMENT]

        Arguments:
           ISSUE    Issue tag or ID

        Options:
           -m, --comment COMMENT      Add a comment
        """

        issue, name = self.getissue(args.ISSUE)

        if issue.status == flags.IN_PROGRESS:
            self.error("already marked as", flags.STATUS[issue.status])

        self.write("Starting work on %s: %s" % (name, issue.title))
        comment = self.getcomment(args.comment)

        self.db.set_status(issue, flags.IN_PROGRESS, comment=comment)
        self.write("Recorded start of work for", name)

    @ditzcmd
    def do_stop(self, args):
        """
        Command:
           stop -- Stop work on an issue

        Usage:
           stop [ISSUE] [-m COMMENT]

        Arguments:
           ISSUE    Issue tag or ID

        Options:
           -m, --comment COMMENT      Add a comment
        """

        issue, name = self.getissue(args.ISSUE)

        if issue.status == flags.PAUSED:
            self.error("already marked as", flags.STATUS[issue.status])

        self.write("Stopping work on %s: %s" % (name, issue.title))
        comment = self.getcomment(args.comment)

        self.db.set_status(issue, flags.PAUSED, comment=comment)
        self.write("Recorded stopping of work for", name)

    @ditzcmd
    def do_assign(self, args):
        """
        Command:
           assign -- Assign an issue to a release

        Usage:
           assign [ISSUE] [-r RELEASE] [-m COMMENT]

        Arguments:
           ISSUE    Issue tag or ID

        Options:
           -r, --release RELEASE      Release to assign it to
           -m, --comment COMMENT      Add a comment
        """

        issue, name = self.getissue(args.ISSUE)

        if issue.release:
            self.write("Issue %s currently assigned to release %s"
                       % (name, issue.release))
        else:
            self.write("Issue %s not currently assigned to any release" % name)

        release = self.getrelease(args.release)

        if not release:
            releases = self.db.project.releases
            choices = [r.name for r in releases
                       if r.status == flags.UNRELEASED]

            if issue.release and issue.release in choices:
                choices.remove(issue.release)

            if not choices:
                self.error("no other release available")

            if len(choices) > 1:
                release = self.getchoice("release", choices)
            else:
                release = choices[0]

        if release == issue.release:
            self.error("already assigned to release %s" % release)

        if not self.db.get_release(release):
            self.error("no release with name '%s'" % release)

        self.write("Assigning to release", release)
        comment = self.getcomment(args.comment)

        self.db.set_release(issue, release, comment=comment)
        self.write("Assigned", name, "to", release)

    @ditzcmd
    def do_unassign(self, args):
        """
        Command:
           unassign -- Unassign an issue from any releases

        Usage:
           unassign [ISSUE] [-m COMMENT]

        Arguments:
           ISSUE    Issue tag or ID

        Options:
           -m, --comment COMMENT      Add a comment
        """

        issue, name = self.getissue(args.ISSUE)

        if not issue.release:
            self.error("not assigned to a release")

        relname = issue.release
        self.write("Unassigning %s: %s" % (name, issue.title))
        comment = self.getcomment(args.comment)

        self.db.set_release(issue, None, comment=comment)
        self.write("Unassigned", name, "from", relname)

    @ditzcmd
    def do_claim(self, args):
        """
        Command:
           claim -- Claim an issue for yourself

        Usage:
           claim [ISSUE] [-m COMMENT]

        Arguments:
           ISSUE    Issue tag or ID

        Options:
           -m, --comment COMMENT      Add a comment
        """

        issue, name = self.getissue(args.ISSUE)

        self.write("Claiming %s: %s" % (name, issue.title))
        claimer = self.db.config.username

        if issue.claimer:
            if issue.claimer == claimer:
                self.error("already claimed by you")

            if not self.getyesno("Issue already claimed by %s.  "
                                 "Claim it anyway?" % issue.claimer):
                return

        comment = self.getcomment(args.comment)
        self.db.claim_issue(issue, claimer=claimer, comment=comment,
                            force=True)

        self.write("Claimed issue %s: %s" % (name, issue.title))

    @ditzcmd
    def do_unclaim(self, args):
        """
        Command:
           unclaim -- Unclaim a claimed issue

        Usage:
           unclaim [ISSUE] [-m COMMENT]

        Arguments:
           ISSUE    Issue tag or ID

        Options:
           -m, --comment COMMENT      Add a comment
        """

        issue, name = self.getissue(args.ISSUE)

        self.write("Unclaiming %s: %s" % (name, issue.title))
        claimer = self.db.config.username

        if not issue.claimer:
            self.error("Issue is not claimed")

        if issue.claimer != claimer:
            if not self.getyesno("Issue can only be unclaimed by %s.  "
                                 "Unclaim it anyway?" % issue.claimer):
                return

        comment = self.getcomment(args.comment)
        self.db.unclaim_issue(issue, claimer=claimer, comment=comment,
                              force=True)

        self.write("Unclaimed issue %s: %s" % (name, issue.title))

    @ditzcmd
    def do_close(self, args):
        """
        Command:
           close -- Close an issue

        Usage:
           close [ISSUE] [-D DISP] [-m COMMENT]

        Arguments:
           ISSUE    Issue tag or ID

        Options:
           -D, --disposition DISP     Set disposition (fixed, wontfix, reorg)
           -m, --comment COMMENT      Add a comment
        """

        issue, name = self.getissue(args.ISSUE)

        self.write("Closing issue %s: %s" % (name, issue.title))

        disp = flags.DISPOSITION
        revdisp = {disp[x]: x for x in disp}
        choices = (disp[flags.FIXED], disp[flags.WONTFIX], disp[flags.REORG])

        choice = args.disposition or self.getchoice("disposition", choices)
        disp = revdisp.get(choice, None)

        if not disp:
            self.error("no such disposition: %s" % disp)

        comment = self.getcomment(args.comment)

        self.db.set_status(issue, flags.CLOSED, disposition=disp,
                           comment=comment)

        self.write("Closed issue", name, "with disposition", choice)

    @ditzcmd
    def do_drop(self, args):
        """
        Command:
           drop -- Drop an issue

        Usage:
           drop [ISSUE]

        Arguments:
           ISSUE    Issue tag or ID

        Details:
           This command removes the issue from the database entirely.
           Other issue tags may change.
        """

        issue, name = self.getissue(args.ISSUE)

        self.db.drop_issue(issue)
        self.write("Dropped %s.  Other issue names may have changed." % name)
