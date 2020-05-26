from preapp import Node, ConfirmQuestion
from preapp.utils.fileio import get_all_assets


class FeaturesNode(Node):
    """Allows users to select features for their apps"""

    def __init__(self):
        super(FeaturesNode, self).__init__("features", [], parents=["platform"])

    def pre_process(self):
        # get all json files in assets/features
        features: List[str] = get_all_assets("features", "json", False, False)
        # create questions
        for feature in features:
            self.add_question(ConfirmQuestion(feature, f"Do you want to include {feature}?", False))

    def post_process(self, responses):
        # add included features sub nodes
        for key, value in responses.items():
            if value and key != "serializable":
                self.add_child(key)


Node.register(FeaturesNode())
