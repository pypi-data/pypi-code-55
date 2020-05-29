"""
Project commands.
"""

from .utils import ditzcmd


class CmdProject(object):
    @ditzcmd
    def do_add_component(self, args):
        """
        Command:
           add-component -- Add a component

        Usage:
           add-component [NAME]

        Arguments:
           NAME     Component name
        """

        name = args.NAME or self.getline("Name: ", allowempty=False)

        self.db.add_component(name)
        self.write("Added component", name)

    @ditzcmd
    def do_add_release(self, args):
        """
        Command:
           add-release -- Add a release

        Usage:
           add-release [NAME] [-m COMMENT]

        Arguments:
           NAME                       Release name

        Options:
           -m, --comment COMMENT      Add a comment
        """

        name = args.NAME or self.getline("Name: ", allowempty=False)

        self.write("Adding release", name)
        comment = self.getcomment(args.comment)
        self.db.add_release(name, comment=comment)
        self.write("Added release", name)

    @ditzcmd
    def do_release(self, args):
        """
        Command:
           release -- Release a release

        Usage:
           release NAME [-m COMMENT]

        Arguments:
           NAME                       Release name

        Options:
           -m, --comment COMMENT      Add a comment
        """

        name = self.getrelease(args.NAME)
        comment = self.getcomment(args.comment)
        self.db.release_release(name, comment)
        self.write("Released", name)

    @ditzcmd
    def do_export(self, args):
        """
        Command:
           export -- Export issue database

        Usage:
           export FORMAT [PATH]
           export --list

        Arguments:
           FORMAT   Export format
           PATH     Path to export to

        Options:
           -l, --list     List the available export formats
        """

        if not args.list:
            fmt = args.FORMAT
            path = args.PATH or fmt
            self.db.export(fmt, path)
            self.write("Exported issues to '%s'" % path)
        else:
            from ditz.exporter import get_exporters
            for name, desc in get_exporters():
                self.write("%s -- %s" % (name, desc))

    @ditzcmd
    def do_archive(self, args):
        """
        Command:
           archive -- Archive a release

        Usage:
           archive RELEASE [PATH]

        Arguments:
           RELEASE   Release to archive
           PATH      Path to archive to
        """

        name = args.RELEASE
        path = args.PATH or "ditz-archive-%s" % name

        self.db.archive_release(name, path)
        self.write("Archived to", path)

    @ditzcmd
    def do_validate(self, args):
        """
        Command:
           validate -- Fix or report database problems

        Usage:
           validate
        """

        changes = self.db.validate()

        if changes:
            for idx, msglist in sorted(changes.items()):
                for msg in msglist:
                    self.write("issue %s: %s" % (idx, msg))
        else:
            self.write("No problems found")
