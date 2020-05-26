from .. import Node, InputQuestion, ListQuestion
from github import Github


class MetadataNode(Node):
    """Collects metadata about a software project """

    def __init__(self):
        super(MetadataNode, self).__init__(
            "metadata",
            [
                InputQuestion("name", "Enter the name of the project"),
                InputQuestion("description", "Enter a short description about the project"),
                InputQuestion("owner", "Enter the name of the owner of the project"),
                InputQuestion("owner_email", "Enter the email of the project owner"),
                ListQuestion(
                    "license",
                    "Choose a license for your project",
                    ["[" + item.key + "]: " + item.name for item in Github().get_licenses()],
                ),
            ],
            priority=-1,
        )

    def post_process(self, responses):
        # add the version attribute (default version is 0.0.1)
        self.add_attribute({"version": "0.0.1"})


Node.register(MetadataNode())
