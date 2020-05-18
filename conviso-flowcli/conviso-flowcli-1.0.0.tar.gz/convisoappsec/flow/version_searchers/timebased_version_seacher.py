import git

from .version_searcher_result import VersionSearcherResult


GIT_TAG_ARGS = ('--list', '--sort=-taggerdate')

class TimeBasedVersionSearcher(object):
    def __init__(self, repository_dir):
        self.repository_dir = repository_dir


    def find_current_and_previous_version(self):
        g = git.cmd.Git(self.repository_dir)
        tags_output = g.tag(GIT_TAG_ARGS)
        tags = tags_output.splitlines()

        current_tag = None
        previous_tag = None
        tags = tags[:2]

        if len(tags) >= 2:
           (current_tag, previous_tag) = tags
        elif len(tags) == 1:
            current_tag = tags[0]
        else:
            raise Exception("Was not possible find the current tag")

        return VersionSearcherResult(current_tag, previous_tag)