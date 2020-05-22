import math


def sen_tokenizer(text: str, split_set="。!?！？"):
    sen = []
    sen_ind = 0
    for i, cs in enumerate(text):
        if cs in split_set:
            sen.append(cs)
            if len("".join(sen).strip()) > 1:
                yield sen, sen_ind, len(sen)
            # yield sen, sen_ind, len(sen)
            sen = []
            sen_ind = i + 1
        else:
            sen.append(cs)
    else:
        if len("".join(sen).strip()) > 1:
            yield sen, sen_ind, len(sen)


def min_len_sen_tokenizer(text: str, split_set="。!?！？", minlen=128):
    """
    句子切分， 同时设置切分长度， 当单句过长时进行分割
    :param text:
    :param split_set:
    :param minlen:
    :return:
    """
    for sen_s in sen_tokenizer(text, split_set):
        sen_text, sen_ind, sen_len = sen_s
        if len(sen_text) < minlen:
            yield sen_s
        else:
            # 次数
            subnub = math.ceil(len(sen_text) / minlen)
            # 每次的长度
            step = math.ceil(len(sen_text)/subnub)
            for i in range(0, len(sen_text), step):
                sub_sen_text = sen_text[i: i+step]
                sub_sen_len = len(sub_sen_text)
                sub_sen_ind = sen_ind + i
                yield sub_sen_text, sub_sen_ind, sub_sen_len


