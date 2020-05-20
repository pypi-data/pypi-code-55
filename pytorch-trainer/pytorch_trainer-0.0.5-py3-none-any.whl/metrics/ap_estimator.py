from pytorch_trainer.utils import VOCEvaluator, AverageMeter
from pytorch_trainer.metrics.base_metric import BaseMetric

class APEstimator(BaseMetric):
    def __init__(self, classes):
        self.classes = classes
        self.metrics = AverageMeter()
        self.evaluator = None

    def reset(self):
        self.metrics.reset()
        self.evaluator = VOCEvaluator(self.classes)

    def update_value(self, pred, target):
        """Computes AP
        """
        self.evaluator.add_sample(pred, target)

    def calculate_value(self):
        """Computes AP
        """
        aps = self.evaluator.evaluate()
        for class_idx in range(len(self.classes)):
            if self.classes[class_idx] == '__background__':
                continue
            if len(aps) > class_idx - 1:
                self.metrics.update(aps[class_idx - 1])
            else:
                self.metrics.update(0.0)

    def get_metric_value(self):
        metrics = {}
        metrics["mAP"] = self.metrics.avg
        return metrics