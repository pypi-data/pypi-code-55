import collections


def qa_exact_score(a_gold, a_pred):
    """计算文本片段之间的exact匹配得分
    :param a_gold: scalar，pd.Series or iterable value
        ground truth data
    :param a_pred: scalar，pd.Series or iterable value
        prediction data
    :return: score
    """
    if hasattr(a_gold, '__iter__'):
        assert len(a_gold) == len(a_pred)
        # make sure a_gold and a_pred can access by index
        a_gold, a_pred = list(a_gold), list(a_pred)
        total = len(a_gold)
        num_exact = 0
        for i in range(total):
            if a_gold[i] == a_pred[i]:
                num_exact += 1
        return round(num_exact / total, 2)
    if a_gold == a_pred:
        return 1
    else:
        return 0


def qa_f1_score(a_gold, a_pred):
    """计算文本片段之间的F1得分，按字符计算
    :param a_gold:
    :param a_pred:
    :return:
    """
    def _compute_f1(a_gold, a_pred):
        common = collections.Counter(a_gold) & collections.Counter(a_pred)
        num_same = sum(common.values())
        if a_gold == '':
            return int(a_gold == a_pred)
        if num_same == 0:
            return 0
        precision = 1.0 * num_same / len(a_gold)
        recall = 1.0 * num_same / len(a_pred)
        f1 = (2 * precision * recall) / (precision + recall)
        return f1

    if hasattr(a_gold, '__iter__'):
        assert len(a_gold) == len(a_pred)
        # make sure a_gold and a_pred can access by index
        a_gold, a_pred = list(a_gold), list(a_pred)
        total = len(a_gold)
        sum_f1 = 0
        for i in range(total):
            sum_f1 += _compute_f1(a_gold[i], a_pred[i])
        return round(sum_f1 / total, 2)
    return round(_compute_f1(a_gold, a_pred), 2)
