import git
import warnings

from convisoappsec.flow.versioning_style import semantic_versioning

from .version_searcher_result import VersionSearcherResult


GIT_TAG_ARGS = ('--list')

class SortedByVersioningStyle(object):
    SEMANTIC_VERSIONING_STYLE = 'semantic-versioning'
    STYLES = [
        SEMANTIC_VERSIONING_STYLE,
    ]

    def __init__(self, repository_dir, ignore_prefix, style, current_tag, suppress_warnings=True):
        self.repository_dir = repository_dir
        self.ignore_prefix = ignore_prefix
        self.style = style
        self.current_tag = current_tag
        self.suppress_warnings = suppress_warnings


    def find_current_and_previous_version(self):
        g = git.cmd.Git(self.repository_dir)
        tags_output = g.tag(GIT_TAG_ARGS)
        tags = tags_output.splitlines()

        versions = []

        for tag in tags:
            try:
                versions.append(
                    semantic_versioning.Version(
                      tag,
                      prefix=self.ignore_prefix,
                    )
                )
            except ValueError as e:
                if not self.suppress_warnings:
                    warnings.warn(str(e))

        if not self.current_tag:
            raise Exception(
                'Empty current_tag functionality not implemented yet!'
            )

        current_version = semantic_versioning.Version(
            self.current_tag,
            prefix=self.ignore_prefix,
        )

        previous_version = current_version.find_previous(versions)

        current_tag = str(current_version)
        previous_tag = "INIT-%s" % current_tag

        if previous_version:
            previous_tag = str(previous_version)

        return VersionSearcherResult(
            current_tag, previous_tag
        )
