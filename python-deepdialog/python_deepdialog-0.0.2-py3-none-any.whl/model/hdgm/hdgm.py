from deepdialog.model import AbstractModel


class HDGMModel(AbstractModel):
    def build_graph(self):
        pass

    def prepare_io(self):
        pass

    def prepare_loss(self):
        pass

    def batch_2_feed(self, batch):
        pass

    def __init__(self):
        AbstractModel.__init__()