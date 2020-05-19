from orbis_plugin_metrics_binary_classification_metrics.main import Main
from .confusion_matrices import matrices


def test_get_precision():
    for matrix in matrices:
        true_positive = matrix["tp"]
        false_positive = matrix["fp"]
        result = Main.get_precision(true_positive, false_positive)
    assert result == matrix["precision"]


def test_get_recall():
    for matrix in matrices:
        true_positive = matrix["tp"]
        item_sum = matrix["tp"] + matrix["fn"]
        result = Main.get_recall(true_positive, item_sum)
        assert result == matrix["recall"]


def test_get_f1_score():
    for matrix in matrices:
        precision = matrix["precision"]
        recall = matrix["recall"]
        result = Main.get_f1_score(precision, recall)
        assert result == matrix["f1"]
