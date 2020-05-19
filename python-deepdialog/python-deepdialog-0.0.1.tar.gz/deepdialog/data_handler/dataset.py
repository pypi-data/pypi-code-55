import os
import numpy as np
from itertools import chain
from deepdialog.data_handler.data_utils import clean_sentence_fn
from deepdialog.data_handler.data_utils import build_vocab_fn
from deepdialog.data_handler.data_utils import load_vocab_fn


__ALL__ = ['BaseDataset', 'DialogDataset']


class BaseDataset(object):
    """
    The :class:`BaseDataset` is the base class for loading and pre-processing text datasets.
    It supports reading text/text-related data from files of various formats, cleaning texts, and building vocabulary.

    The typical input for a :class:`BaseDataset` class is the path of dataset.
    Under the dataset_path, at least one file named ``texts.txt`` (or other formats) is supposed to be prepared.
    Within the ``texts.txt`` file, each line contains one data instance, which is a complete text
    (e.g., a dialogue, a document or a sentence).

    There are also cases where labels are required.
    :class:`BaseDataset` provides utilities for loading labels along with texts.
    Label files named ``xxx_labels.txt`` should be prepared in the same dataset_path directory.
    Within each ``xxx_labels.txt`` file, each line contains the label associating with the text data of the same line.
    Users could also provide more than one label files.

    When the given dataset_path contains no appropriate files, `FileNotFoundError` will be raised.

    Parameters
    ===========
    dataset_path: a string
        The directory path of dataset.
    max_vocab_size: an integer
        The maximum size of vocabulary to be built. If there are more than `max_vocab_size` words, words with low
        frequencies will be ignored. Default to be -1, which means no limits.
    label_name_list: a list
        The name list of text attributes to be considered.
        Each name ``xxx`` corresponds to one label file ``xxx_labels.txt``.
    prev_list: a list
        The prefix list of vocabulary. Usually they are manually-designated special tokens.
        Default to be an empty string.
    lowercase: boolean
        If true, transform all words into lowercase. Default to be False.
    rep_num: boolean
        If true, replace numbers with `<num>` token. Default to be False.
    rm_punc: boolean
        If true, remove all punctuation marks. Default to be False.
    """
    def __init__(self,
                 dataset_path,
                 max_vocab_size=-1,
                 prev_list=[],
                 label_name_list=[],
                 lowercase=True,
                 rep_num=True,
                 rm_punc=True):

        self._dataset_path = dataset_path
        self._max_vocab_size = max_vocab_size
        self._label_name_list = label_name_list
        self._lowercase = lowercase
        self._rep_num = rep_num
        self._rm_punc = rm_punc
        self._prev_list = prev_list

        self._data_size = -1
        self._vocab_size = -1

        # read texts
        self._raw_texts = self.read_texts()

        # clean texts
        self._cleaned_texts = self.clean_texts()

        # build vocabulary
        self._word2id, self._id2word = self.build_vocab()

        # read labels
        self._labels_list = self.read_labels()
        self._label2id_list, self._id2label_list = self.build_label_vocab()


    @property
    def dataset_path(self):
        """
        A string. Get current dataset path.
        """
        return self._dataset_path

    @property
    def max_vocab_size(self):
        """
        An integer. Get manually designated maximum size of vocabulary.
        """
        return self._max_vocab_size

    @property
    def label_name_list(self):
        """
        A list of strings. Get available attribute names.
        """
        return self._label_name_list

    @property
    def vocab_size(self):
        """
        An integer. Get the actual vocabulary size.
        """
        if self._vocab_size == -1:
            raise ValueError("No vocabulary built.")
        return self._vocab_size

    @property
    def data_size(self):
        """
        An integer. Get the number of total data instances.
        """
        return self._data_size

    def read_texts(self):
        """
        Read text data from `dataset_path/texts.txt`.

        Returns
        -------
        raw_texts: a list of strings.
            Each string is a line in texts.txt.
        """
        file_path = os.path.join(self._dataset_path, "texts.txt")
        with open(file_path, mode="r", encoding="utf-8") as file:
            raw_texts = file.read().split("\n")
        self._data_size = len(raw_texts)
        return raw_texts


    def clean_texts(self):
        """
        Pre-process raw texts, including transforming into lowercase, replacing numbers with `<num>`,
        replacing urls with `<url>`, and removing punctuations.

        Returns
        -------
        cleaned_texts: a list of strings
            The pre-processed texts.
        """
        cleaned_texts = [clean_sentence_fn(
            sample, lowercase=self._lowercase, rep_num=self._rep_num, rm_punc=self._rm_punc)
                         for sample in self._raw_texts]
        return cleaned_texts


    @property
    def raw_texts(self):
        """
        A list of strings. Get raw texts.
        """
        return self._raw_texts

    @property
    def cleaned_texts(self):
        """
        A list of strings. Get pre-processed texts.
        """
        return self._cleaned_texts

    def build_vocab(self, re_build=True):
        """
        Build the text vocabulary.
        If there's already a ``vocab.txt`` under the `dataset_path`, just load it.
        If not, build it, create ``vocab.txt`` and put it in `dataset_path`.

        Returns
        -------
        word2id: a dict
            Vocabulary that maps from indexes into words.
        id2word: a dict
            Vocabulary that maps from words into indexes.
        """

        vocab_file_path = os.path.join(self._dataset_path, "vocab.txt")
        if os.path.exists(vocab_file_path) and not re_build:
            word2id, id2word = load_vocab_fn(vocab_file_path)

        else:

            word_list = [sent.split() for sent in self._cleaned_texts]
            word_list = list(chain(*word_list))

            word2id, id2word = build_vocab_fn(word_list, self._max_vocab_size, self._prev_list)

            vocab_list = word2id.keys()
            with open(vocab_file_path, mode="w", encoding="utf-8") as file:
                for word in vocab_list:
                    file.write(word + "\n")

        self._vocab_size = len(word2id)
        return word2id, id2word


    @property
    def id2word(self):
        """
        Get a dictionary that maps from indexes into words.
        """
        return self._id2word

    @property
    def word2id(self):
        """
        Get a dictionary that maps from words into indexes.
        """
        return self._word2id

    def read_labels(self):
        """
        Read labels from {name}_labels.txt.

        Returns
        -------
        labels_list: a list of list of strings
            A list that contains multiple label list.
            Each label list is a list of strings, associating with one attribute.
            Each string represents a label value.
        """
        labels_list = []
        for name in self._label_name_list:
            label_file_path = os.path.join(self._dataset_path, name + "_labels.txt")
            with open(label_file_path, mode="r", encoding="utf-8") as file:
                labels = file.read().split("\n")
                assert len(labels) == self._data_size
                labels_list.append(labels)
        return labels_list


    def build_label_vocab(self, re_build=True):
        """
        Build the label vocabulary.
        If there's already a ``{label}_vocab.txt`` under the `dataset_path`, just load it.
        If not, build it, create ``{label}_vocab.txt`` and put it in `dataset_path`.

        Returns
        -------
        label2id_list: a list of dicts
            A list of label vocabularies.
            Each vocabulary associates with one attribute and maps from label values to indexes.
        id2label_list: a list of dicts
            A list of label vocabularies.
            Each vocabulary associates with one attribute and maps from indexes to label values.

        """
        label2id_list = []
        id2label_list = []
        for label_idx, name in enumerate(self._label_name_list):
            label_file_path = os.path.join(self._dataset_path, name + "_vocab.txt")
            if os.path.exists(label_file_path) and not re_build:
                label2id, id2label = load_vocab_fn(label_file_path)

            else:

                word_list = self._labels_list[label_idx]
                label2id, id2label = build_vocab_fn(word_list)

                label_list = label2id.keys()
                with open(label_file_path, mode="w", encoding="utf-8") as file:
                    for word in label_list:
                        file.write(word + "\n")

            label2id_list.append(label2id)
            id2label_list.append(id2label)

        return label2id_list, id2label_list


    @property
    def labels_list(self):
        return self._labels_list

    @property
    def label2id_list(self):
        return self._label2id_list

    @property
    def id2label_list(self):
        return self._id2label_list


class DialogDataset(BaseDataset):
    """
    The :class:`DialogDataset` is a class particularly for dialogue dataset processing.
    It inherits the parent class :class:`BaseDataset`.
    In addition to basic operation for text processing,
    :class:`DialogDataset` class also has dialogue-specific operations,
    including adding special tokens, splitting dialogues according to its word-utterance-dialogue hierarchy,
    and computing its relevant statistics.

    Parameters
    ===========
    dataset_path: a string
        The directory path of dataset.
    max_vocab_size: an integer
        The maximum size of vocabulary to be built. If there are more than `max_vocab_size` words, words with low
        frequencies will be ignored. Default to be -1, which means no limits.
    label_name_list: a list
        The name list of text attributes to be considered.
        Each name ``xxx`` corresponds to one label file ``xxx_labels.txt``.
    lowercase: boolean
        If true, transform all words into lowercase. Default to be False.
    rep_num: boolean
        If true, replace numbers with `<num>` token. Default to be False.
    rm_punc: boolean
        If true, remove all punctuation marks. Default to be False.

    """
    def __init__(self,
                 dataset_path,
                 turn_separator,
                 max_vocab_size=-1,
                 label_name_list=[],
                 lowercase=True,
                 rep_num=True,
                 rm_punc=True):
        BaseDataset.__init__(self, dataset_path, max_vocab_size, ["<pad>", "<unk>", "<sos>", "<eos>"],
                             label_name_list, lowercase, rep_num, rm_punc)

        self._turn_separator = turn_separator
        self._pad_id = self.word2id["<pad>"]
        self._unk_id = self.word2id["<unk>"]
        self._sos_id = self.word2id["<sos>"]
        self._eos_id = self.word2id["<eos>"]

        self._dialog_data = self.split_data()

        self.print_stats()

    @property
    def turn_separator(self):
        """
        A string. The special token that separates dialogue turns.
        It is supposed to present in the given dialogue dataset.
        """
        return self._turn_separator

    @property
    def pad_id(self):
        """
        An integer. The index number of `<pad>` token.
        """
        return self._pad_id

    @pad_id.setter
    def pad_id(self, value):
        if value != 0 or not isinstance(value, int):
            raise ValueError("pad_id is supposed to be integer 0.")
        self._pad_id = value

    @property
    def unk_id(self):
        """
        An integer. The index number of `<unk>` token.
        It represents all out-of-vocabulary words.
        """
        return self._unk_id

    @property
    def eos_id(self):
        """
        An integer. The index number of `<eos>` token.
        It represents the end-of-sentence.
        """
        return self._eos_id

    @property
    def sos_id(self):
        """
        An integer. The index number of `<sos>` token.
        It represents the start-of-sentence.
        """
        return self._sos_id

    def split_data(self):
        """
        Split dialogue data according to the word-utterance-dialog hierarchy.

        Returns
        -------
        dialog_data: A list of list of list of strings
            The dialogue data that have been split.
            The outer list represents the whole dataset.
            The medium list represents each dialogue, consisting of multiple utterances.
            The inner list represents each utterance, consisting of multiple words.
        """
        dialog_data = [[sent.split() for sent in dial.split(self._turn_separator)] for dial in self._cleaned_texts]

        return dialog_data

    @property
    def dialog_data(self):
        """
        Get the split dialog data.
        """
        return self._dialog_data

    def print_stats(self):
        """
        Compute and print basic statistics of the dialogue dataset,
        including total data size, average turns per dialogue, average lengths per turn, and vocabulary size.
        """
        print("===========================================")
        print("Statistics of dialogue dataset in %s." % self._dataset_path)
        print("===========================================")

        print("[*] Total data size: %d" % self._data_size)

        turns = [len(dial) for dial in self._dialog_data]
        print("[*] Max#turn: %d, Min#turn: %d, Avg turn per dialog: %.4f" % (np.max(turns), np.min(turns),
                                                                           np.mean(turns)))

        lens = [len(turn) for dial in self._dialog_data for turn in dial]
        print("[*] avg lengths per turn: %.4f" % np.mean(lens))

        print("[*] vocab size: %d" % self._vocab_size)


class TranslationDataset(BaseDataset):
    pass

class SummarizationDataset(BaseDataset):
    pass