"""
Data validation schemas.
"""

from __future__ import print_function

from cerberus import Validator

from .flags import TYPE, STATUS, RELSTATUS, DISPOSITION


class DitzValidator(Validator):
    def __init__(self, *args, **kwargs):
        if 'additional_context' in kwargs:
            self.additional_context = kwargs['additional_context']
        super(DitzValidator, self).__init__(*args, **kwargs)

    def _validate_type_none(self, value):
        if value is None:
            return True


def string(**kw):
    kw.update(type='string')
    return kw


def option(iterable, **kw):
    kw.update(type='string', allowed=list(iterable))
    return kw


def datetime(**kw):
    kw.update(type='datetime')
    return kw


def release(**kw):
    kw.update(type=['number', 'string', 'none'], coerce=to_release)
    return kw


def to_release(v):
    return str(v) if v is not None else None


def listof(schema, **kw):
    kw.update(type='list', schema=schema)
    return kw


event = {'type': 'list',
         'items': [datetime(), string(), string(), string()]}

issue = {'title': string(required=True, empty=False),
         'desc': string(required=True),
         'type': option(TYPE.keys(), required=True),
         'component': string(required=True),
         'release': release(required=True, default=None, nullable=True),
         'reporter': string(required=True),
         'claimer': string(default=None, nullable=True),
         'status': option(STATUS.keys(), required=True),
         'disposition': option(DISPOSITION.keys(), required=True,
                               nullable=True),
         'creation_time': datetime(required=True),
         'references': listof(string(), required=True),
         'id': string(required=True, regex=r'[0-9a-f]{40}'),
         'log_events': listof(event, required=True)}

component = {'name': string(required=True, empty=False)}

release = {'name': string(required=True, empty=False),
           'status': option(RELSTATUS.keys(), nullable=True),
           'release_time': datetime(required=True, nullable=True),
           'log_events': listof(event)}

project = {'name': string(required=True, empty=False),
           'version': string(required=True),
           'components': listof(component, required=False),
           'releases': listof(release)}

schemas = {'issue': issue,
           'release': release,
           'component': component,
           'project': project}

project_validator = DitzValidator(project)
release_validator = DitzValidator(release)
component_validator = DitzValidator(component)
issue_validator = DitzValidator(issue)
