#!/usr/bin/env python
#   This file is part of nexdatas - Tango Server for NeXus data writer
#
#    Copyright (C) 2012-2018 DESY, Jan Kotanski <jkotan@mail.desy.de>
#
#    nexdatas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nexdatas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nexdatas.  If not, see <http://www.gnu.org/licenses/>.
#

""" gitlab tools for converting an svn repoitory to a local git repository"""

import subprocess
import sys
import os
import argparse


class GLFromSVN(object):

    """ GitLab Create a local git repository from an svn repository"""

    def __init__(self, options):
        """ the main program function

        :param options: parser options
        :type options: :class:`argparse.Namespace`
        """
        self.__trunk = options.trunk or "trunk"
        self.__branches = options.branches or "branches"
        self.__tags = options.tags or "tags"
        self.__svnurl = options.svnurl or \
            "https://svn.code.sf.net/p/tango-ds/code/"
        self.__svndir = options.args[0] if len(options.args) > 0 else ""
        self.__url = "%s/%s" % (self.__svnurl, self.__svndir) \
                     if self.__svndir else options.url
        self.__localdir = options.localdir or self.__url.split("/")[-1]
        self.__authors = options.authors or "./authors.txt"
        if not os.path.exists(self.__authors):
            print("Warning: %s does not exists" % self.__authors)
            self.__authors = ""
        self.__tagmessage = options.tagmessage or "migrate svn to git"

    def run(self):
        """ the main program function
        """
        # fetch all subgroups
        clonecmd = 'git svn clone %s %s -T %s -b %s -t %s ' \
                   % (self.__url, self.__localdir, self.__trunk,
                      self.__branches, self.__tags)
        if self.__authors:
            clonecmd += '--authors-file=%s' % self.__authors
        tagcmd = 'cd %s;' \
                 ' \git for-each-ref refs/remotes/origin/tags |' \
                 ' cut -d / -f 5-|' \
                 ' while read ref; ' \
                 ' do git tag -a "$ref" -m"%s" ' \
                 '        "refs/remotes/origin/tags/$ref" && '\
                 '     echo "Add a new tag: $ref"; ' \
                 ' done' % (self.__localdir, self.__tagmessage)
        branchcmd = 'cd %s;' \
                    'git for-each-ref refs/remotes/origin  | ' \
                    'grep -v trunk | grep -v tag |  cut -d / -f 4-| ' \
                    'while read ref; ' \
                    'do git checkout origin/$ref -b $ref &&' \
                    '      echo "Add a new branch:  $ref"; '\
                    'done' % (self.__localdir)
        commands = [clonecmd, tagcmd, branchcmd]
        if self.__url:
            for cmd in commands:
                try:
                    print(cmd)
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        shell=True)
                    proc_stdout = process.communicate()[0].strip()
                    if hasattr(proc_stdout, "decode"):
                        print(proc_stdout.decode())
                except Exception as e:
                    print("Error: %s" % (str(e)))


def main():
    """ the main program function
    """

    #: pipe arguments
    pipe = ""
    if not sys.stdin.isatty():
        pp = sys.stdin.readlines()
        #: system pipe
        pipe = "".join(pp)

    description = "Command-line tool create a local git repository" \
                  " from a given svn repository"

    epilog = 'examples:\n' \
        '  glfromsvn DeviceClasses/CounterTimer/DGG2 \n\n' \
        '    - create a local git repository in "DGG2" directory ' \
        'and fetch authors emails from "./authors.txt" \n\n' \

    parser = argparse.ArgumentParser(
        description=description, epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        'args', metavar='svndir', type=str, nargs='?',
        help='svn group directory, '
        'e.g. "DeviceClasses/CounterTimer/DGG2"')
    parser.add_argument(
        "-T", "--trunk",
        help='trunk svn directory, default: trunk',
        dest="trunk", default="trunk")
    parser.add_argument(
        "-b", "--branches",
        help='branch svn directory, default: branches',
        dest="branches", default="branches")
    parser.add_argument(
        "-t", "--tags",
        help='tag svn directory, default: tags',
        dest="tags", default="tags")
    parser.add_argument(
        "-s", "--svn-url",
        help='root svn url, '
        'default: "https://svn.code.sf.net/p/tango-ds/code/"',
        dest="svnurl",
        default="https://svn.code.sf.net/p/tango-ds/code/")
    parser.add_argument(
        "-u", "--url",
        help='full svn url with svn project directory, '
        'e.g.: "https://svn.code.sf.net/p/tango-ds/code/'
        'DeviceClasses/CounterTimer/DGG2"',
        dest="url",
        default="")
    parser.add_argument(
        "-l", "--local-dir",
        help='local git directory, e.g.: "DGG2"',
        dest="localdir",
        default="")
    parser.add_argument(
        "-a", "--authors",
        help='file with authors, '
        'default: "./authors.txt"',
        dest="authors", default="./authors.txt")
    parser.add_argument(
        "-m", "--tag-message",
        help='tag message, '
        'default: "migrate svn to git"',
        dest="tagmessage", default="")

    try:
        options = parser.parse_args()
    except Exception as e:
        sys.stderr.write("Error: %s\n" % str(e))
        sys.stderr.flush()
        parser.print_help()
        print("")
        sys.exit(255)

    #: command-line and pipe arguments
    parg = []
    if hasattr(options, "args"):
        parg = [options.args] if options.args else []
    if pipe:
        parg.append(pipe)
    options.args = parg

    if not options.args and not options.url:
        parser.print_help()
        print("")
        sys.exit(255)

    try:
        command = GLFromSVN(options)
        command.run()
    except Exception as e:
        sys.stderr.write("Error: glfromsvn interrupted with:")
        sys.stderr.write(str(e))
        sys.stderr.flush()
        sys.exit(255)


if __name__ == "__main__":
    main()
