"""
Internal Ditz objects.
"""

import os
import re
import hashlib
import random
import six

from datetime import datetime, timedelta
from functools import total_ordering
from distutils.version import LooseVersion

from .util import (check_value, to_unicode,
                   default_name, default_email, DitzError)

from .flags import (STATUS, RELSTATUS, RELEASED, UNRELEASED, BUGFIX,
                    FEATURE, TASK, DISPOSITION, UNSTARTED, TYPE, SORT,
                    CLOSED)

from .files import DitzObject, read_object_file
from .config import config

from . import schemas

# Regexp matching start of progress on an issue.
re_start = re.compile(r'to in.progress')

# Regexp matching end of progress on an issue.
re_stop = re.compile(r'(from in.progress|closed with disposition)')


class Project(DitzObject):
    yaml_tag = DitzObject.ditz_tag + '/project'
    validator = schemas.project_validator
    filename = "project.yaml"

    #: Attributes that get saved to file.
    attributes = ["name", "version", "components", "releases"]

    #: Name of the project.
    name = ""

    #: List of components.  Each entry is a :class:`Component`.
    components = []

    #: List of releases.  Each entry is a :class:`Release`.
    releases = []

    def __init__(self, name, version="0.5"):
        self.name = to_unicode(name)
        self.version = version
        self.components = [Component(name)]
        self.releases = []


class Release(DitzObject):
    yaml_tag = DitzObject.ditz_tag + '/release'
    validator = schemas.release_validator

    #: Attributes that get saved to file.
    attributes = ["name", "status", "release_time", "log_events"]

    #: Name of the release.
    name = None

    #: Time it was released, or None.
    release_time = None

    #: List of log events.  Each entry is a tuple of (time, username, text,
    #: comment).
    log_events = []

    def __init__(self, name, status=UNRELEASED, release_time=None):
        self.name = to_unicode(name)
        self.status = status
        self.release_time = release_time
        self.log_events = []

        self.set_status(status)

    def set_status(self, status):
        check_value("status", status, RELSTATUS)
        self.status = status

    @property
    def version(self):
        "Tuple representing the release version."
        return LooseVersion(self.name)

    @property
    def released(self):
        "Whether release has actually been released."
        return self.status == RELEASED

    @property
    def description(self):
        if not self.released:
            tag = "unreleased"
        else:
            tag = "released %s" % (self.release_time.strftime("%Y-%m-%d"))

        return "%s (%s)" % (self.name, tag)

    def __repr__(self):
        return "<Release: %s>" % self.name


class Component(DitzObject):
    yaml_tag = DitzObject.ditz_tag + '/component'
    validator = schemas.component_validator
    attributes = ["name"]

    #: Name of the component.
    name = ""

    def __init__(self, name):
        self.name = to_unicode(name)

    def __repr__(self):
        return "<Component: %s>" % self.name


@total_ordering
class Issue(DitzObject):
    yaml_tag = DitzObject.ditz_tag + '/issue'
    validator = schemas.issue_validator
    template = "issue-%s.yaml"

    #: Attributes that get saved to file.
    attributes = ["title", "desc", "type", "component", "release",
                  "reporter", "claimer", "status", "disposition",
                  "creation_time", "references", "id", "log_events"]

    #: List of references.  Each entry is a string.
    references = []

    #: List of log events.  Each entry is a tuple of (time, username, text,
    #: comment).
    log_events = []

    #: Defaults for attributes added since the original set.
    defaults = {'claimer': None}

    def __init__(self, title, desc="", type=BUGFIX, status=UNSTARTED,
                 disposition=None, creation_time=None, reporter=""):
        self.title = to_unicode(title.strip())
        self.desc = to_unicode(desc.strip())
        self.component = None
        self.release = None
        self.claimer = None
        self.reporter = to_unicode(reporter)

        self.set_type(type)
        self.set_status(status)
        self.set_disposition(disposition)

        self.creation_time = creation_time or datetime.now()
        self.id = self.make_id()

        self.references = []
        self.log_events = []

    @property
    def name(self):
        "Name of the issue.  This is the same as its title."
        return self.title

    @property
    def longname(self):
        "Name of the issue, with (bug) or (feature) appended."
        if self.bugfix:
            return self.title + " (bug)"
        elif self.feature:
            return self.title + " (feature)"
        else:
            return self.title

    @property
    def closed(self):
        "Whether the issue is closed."
        return self.status == CLOSED

    @property
    def bugfix(self):
        "Whether the issue is a bugfix."
        return self.type == BUGFIX

    @property
    def feature(self):
        "Whether the issue is a feature."
        return self.type == FEATURE

    @property
    def task(self):
        "Whether the issue is a task."
        return self.type == TASK

    @property
    def filename(self):
        return self.template % self.id

    @property
    def progress_time(self):
        "Total seconds the issue's state has been in-progress."
        total = timedelta()
        start = None

        for time, _, event, _ in self.log_events:
            if re_start.search(event):
                start = time
            elif re_stop.search(event) and start is not None:
                total += time - start
                start = None

        if start is not None:
            total += datetime.now() - start

        return total.total_seconds()

    @property
    def modified_time(self):
        "Time the issue was last modified."
        if self.log_events:
            return self.log_events[-1][0]
        else:
            return self.creation_time

    def set_type(self, type):
        check_value("type", type, TYPE)
        self.type = type

    def set_status(self, status):
        check_value("status", status, STATUS)
        self.status = status

    def set_disposition(self, disposition):
        if disposition:
            check_value("disposition", disposition, DISPOSITION)

        self.disposition = disposition

    def add_reference(self, reference):
        reference = to_unicode(reference)
        self.references.append(reference)
        return len(self.references)

    def grep(self, regexp):
        for attr in "title", "desc", "reporter":
            if regexp.search(getattr(self, attr)):
                return True

        for ref in self.references:
            if regexp.search(ref):
                return True

        for event in self.log_events:
            if regexp.search(event[3]):
                return True

        return False

    def make_id(self):
        data = [self.creation_time, random.random(),
                self.reporter, self.title, self.desc]

        string = "\n".join([six.text_type(item) for item in data])
        return hashlib.sha1(string.encode('utf-8')).hexdigest()

    def __eq__(self, other):
        if hasattr(other, "id"):
            return self.id == other.id

        return False

    def __lt__(self, other):
        this = (SORT[self.status], self.modified_time)
        that = (SORT[other.status], other.modified_time)
        return this < that

    def __hash__(self):
        return int(self.id, 16)

    def __repr__(self):
        return "<Issue: %s>" % self.id


class Config(DitzObject):
    yaml_tag = DitzObject.ditz_tag + '/config'
    filename = ".ditz-config"
    attributes = ["name", "email", "issue_dir"]

    def __init__(self, name, email, issue_dir="issues"):
        self.name = to_unicode(name)
        self.email = to_unicode(email)
        self.issue_dir = issue_dir

    @staticmethod
    def find(basedir=".", error=False, search=True):
        """
        Find Ditz configuration in (or possibly above) a base directory.

        Return the directory and corresponding Config object.
        """

        basedir = os.path.realpath(basedir)
        curdir = basedir

        issuedirs = config.get('config', 'issuedirs').split()

        while True:
            # If Ditz config found, read it.
            path = os.path.join(curdir, Config.filename)
            if os.path.exists(path):
                return curdir, read_object_file(path)

            # If there's an issue directory containing a project file, use
            # that.
            for dirname in issuedirs:
                path = os.path.join(curdir, dirname, Project.filename)
                if os.path.exists(path):
                    name = default_name()
                    email = default_email()
                    conf = Config(name, email, dirname)
                    conf.write()
                    return curdir, conf

            # Otherwise, go to parent directory.
            pardir = os.path.split(curdir)[0]

            # If it's not found, or we're at the top, give up.
            if pardir == curdir or not search:
                if error:
                    where = "in or above" if search else "in"
                    raise DitzError("can't find '%s' %s '%s'"
                                    % (Config.filename, where, basedir))
                else:
                    return None, None

            curdir = pardir

    def write(self, dirname="."):
        """
        Write Ditz config file if required.
        """

        if config.getboolean('config', 'create_ditz_config'):
            super(Config, self).write(dirname)
            return True

        return False

    @property
    def username(self):
        if self.email:
            return "%s <%s>" % (self.name, self.email)
        else:
            return self.name

    def __repr__(self):
        return "<Config: %s>" % self.name
