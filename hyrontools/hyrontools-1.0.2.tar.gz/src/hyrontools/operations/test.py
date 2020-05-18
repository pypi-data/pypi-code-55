import hyron
from .operation import Operation


class TestRulebook(Operation, register="test"):
    """
        Render all artifacts silently.
        Maybe we'll do actual testing one day...
        Usage: hyrontools test [rulebookfile]
    """

    ARGC = 1

    def prepare_args(self, args: tuple):
        loader = hyron.rulebooks.RulebookLoader()
        return {
            "rulebook": loader.load(args[0])
        }

    def run(self, rulebook: hyron.rulebooks.Rulebook):
        self.console.print("Rendering all artifacts...")

        rulebook.build_all()

        self.console.print("Rendering pass complete - all artifacts built!")
