import hyron
from .operation import Operation
from ..errors import ValidationError


class RenderArtifact(Operation, register="render"):
    """
        Render an artifact to console.
        Usage: hyrontools render [rulebookfile] [artifact]
    """

    ARGC = 2

    def prepare_args(self, args: tuple):
        loader = hyron.rulebooks.RulebookLoader()
        return {
            "rulebook": loader.load(args[0]),
            "artifact": args[1],
        }

    def postvalidate(self, rulebook: hyron.rulebooks.Rulebook, artifact: str):
        self.assert_artifacts(rulebook)
        if artifact not in rulebook.artifacts:
            raise ValidationError(
                f"Rulebook '{rulebook.title}' doesn't reference an artifact named '{artifact}'",  # noqa
                False
            )

    def run(self, rulebook: hyron.rulebooks.Rulebook, artifact: str):
        self.console.print(f"Rendering '{artifact}' artifact...")

        artifact = rulebook.build_artifact(artifact)

        self.console.print("Render complete.")

        self.console.print_json("Artifact metadata", artifact.meta)

        self.console.print_iter("File list", artifact.files.keys())

        for name, artifact_file in artifact.files.items():
            encoding = artifact_file.encoding
            self.console.print_title(f"File '{name}'")
            self.console.newln()
            self.console.print(artifact_file.get_contents().decode(encoding))
            self.console.newln()
