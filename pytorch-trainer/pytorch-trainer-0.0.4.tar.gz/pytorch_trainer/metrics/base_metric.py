
from abc import ABC, abstractmethod

class BaseMetric(ABC):
    """
    网络模型质量度量的抽象类
    """
    @abstractmethod
    def update_value(self, output, target):
        """
        更新评估值的抽象类
        """
        pass

    @abstractmethod
    def get_metric_value(self):
        pass

    @abstractmethod
    def reset(self):
        pass