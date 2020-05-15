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

""" gitlab tools for uploading a local git repository to a remote gitlab"""

import subprocess
import sys
import argparse


class GLUpload(object):

    """ GitLab upload a local git repository to a remote gitlab"""

    def __init__(self, options):
        """ the main program function

        :param options: parser options
        :type options: :class:`argparse.Namespace`
        """
        self.__user = options.user
        self.__giturl = options.giturl or \
            "https://eosc-pan-git.desy.de/tango-ds/"
        self.__gitdir = options.args[0] if len(options.args) > 0 else ""
        self.__url = "%s/%s.git" % (self.__giturl, self.__gitdir) \
                     if self.__gitdir else options.url
        self.__localdir = options.localdir or "."

    def run(self):
        """ the main program function
        """

        addcmd = 'cd %s; git remote add gitlab %s' \
            % (self.__localdir, self.__url)
        pushcmd = 'cd %s; git push -u gitlab --all ; ' \
                  'git push -u gitlab --tags' \
                  % self.__localdir
        if self.__user:
            addcmd = addcmd.replace("://", "://%s@" % self.__user)
        commands = [addcmd, pushcmd]
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

    description = "Command-line tool to upload a local git repository" \
                  " to a remote git repository"

    epilog = 'examples:\n' \
        '  glupload DeviceClasses/CounterTimer/DGG2 \n\n' \
        '    - upload a local git repository in the "." directory ' \
        'to https://eosc-pan-git.desy.de/tango-ds/DeviceClasses/' \
        'CounterTimer/DGG2.git \n\n' \

    parser = argparse.ArgumentParser(
        description=description, epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        'args', metavar='group', type=str, nargs='?',
        help='gitlab group, '
        'e.g. "DeviceClasses/CounterTimer/DGG2"')
    parser.add_argument(
        "-g", "--git-url",
        help='root git url, '
        'default: "https://eosc-pan-git.desy.de/tango-ds/"',
        dest="giturl",
        default="https://eosc-pan-git.desy.de/tango-ds/")
    parser.add_argument(
        "-f", "--url",
        help='full git url with git subgroups and a project name, '
        'e.g.: "https://eosc-pan-git.desy.de/tango-ds/'
        'deviceclasses/countertimer/gdd2"',
        dest="url",
        default="")
    parser.add_argument(
        "-u", "--user",
        help="gitlab user",
        dest="user", default="")
    parser.add_argument(
        "-l", "--local-dir",
        help='local git directory, e.g.: "DGG2"',
        dest="localdir",
        default=".")

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
        command = GLUpload(options)
        command.run()
    except Exception as e:
        sys.stderr.write("Error: glupload interrupted with:")
        sys.stderr.write(str(e))
        sys.stderr.flush()
        sys.exit(255)


if __name__ == "__main__":
    main()
