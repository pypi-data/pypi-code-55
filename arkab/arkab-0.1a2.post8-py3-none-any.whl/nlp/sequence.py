from os import path
import re
from collections import Counter


def _tokenized_v2(sent: str):
    # def tokenize(sent):
    #     '''Return the tokens of a sentence including punctuation.
    #     >>> tokenize('Bob dropped the apple. Where is the apple?')
    #     ['Bob', 'dropped', 'the', 'apple', '.', 'Where', 'is', 'the', 'apple', '?']
    #     '''
    # return [x.strip() for x in re.split(r'(\W+)', sent) if x.strip()]
    return re.findall(r'\w+', sent.lower())


def _tokenized_v1(sent: str, ignore_case: bool = False) -> list:
    # "[\w']+"
    """

    :param sent: sentence,
    :param ignore_case: true for lower

    :return: list of words
    """
    if ignore_case:
        sentence = re.sub("[.,!?\\-]", '', sent.lower())
    else:
        sentence = re.sub("[.,!?\\-]", '', sent)
    return sentence.split(" ")


tokenized = _tokenized_v1


class Corpus:
    def __init__(self, src, specials: list = None):
        """

        :param src: source corpus filename
        :param specials: Tokens like <UNK>, <SEP> or so.

        """
        assert path.exists(src) and path.isfile(src), f"Fatal Error! f{src} must be a file"
        with open(src, 'r') as fp:
            self.lines = fp.readlines()
        self.vocabulary = dict()  # TODO: convenient way to build
        if specials is None:
            self.specials = []
        else:
            self.specials = specials

    def build_voc(self):
        """
        TODO: Finish code

        For each line:
        line -> tokenized -> added to counter -> to dict
        """
        counter = Counter()
        for line in self.lines:
            word_bag = tokenized(line, ignore_case=False)
            for w in word_bag:
                counter[w] += 1

        for index, tup in enumerate(counter.most_common()):
            w = tup[0]
            self.vocabulary[w] = index + len(self.specials)


if __name__ == '__main__':
    _sent = "Do you hear the people sing? Can't me sing!"
    print(_tokenized_v2(_sent))
