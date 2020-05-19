# -*- coding: utf-8 -*-
"""Summary

Attributes:
    logger (TYPE): Description
"""

import logging
logger = logging.getLogger(__name__)


class Main(object):

    """Summary
    """

    def __init__(self):
        """Summary
        """
        super(Main, self).__init__()

    @classmethod
    def get_precision(cls, true_positive, false_positive):
        """Summary

        Args:
            true_positive (TYPE): Description
            false_positive (TYPE): Description

        Returns:
            TYPE: Description
        """

        true_positive, false_positive = float(true_positive), float(false_positive)
        try:
            result = (true_positive / (true_positive + false_positive))
        except ZeroDivisionError:
            result = 0
        return result

    @classmethod
    def get_recall(cls, true_positive, item_sum):
        """Summary

        Args:
            true_positive (TYPE): Description
            item_sum (TYPE): Description

        Returns:
            TYPE: Description
        """
        true_positive, item_sum = float(true_positive), float(item_sum)
        try:
            result = (true_positive / item_sum)
        except ZeroDivisionError:
            result = 0
        return result

    @classmethod
    def get_f1_score(cls, precision, recall):
        """Summary

        Args:
            precision (TYPE): Description
            recall (TYPE): Description

        Returns:
            TYPE: Description
        """
        precision, recall = float(precision), float(recall)
        try:
            result = 2 * ((precision * recall) / (precision + recall))
        except ZeroDivisionError:
            result = 0
        return result

    @classmethod
    def get_sensitivity(cls):
        """aka true positive rate

        Raises:
            NotImplemented: Description
        """
        raise NotImplemented

    @classmethod
    def get_specificity(cls):
        """aka true negative rate

        Raises:
            NotImplemented: Description
        """
        raise NotImplemented

    @classmethod
    def get_roc(cls):
        """Summary

        Raises:
            NotImplemented: Description
        """
        raise NotImplemented
