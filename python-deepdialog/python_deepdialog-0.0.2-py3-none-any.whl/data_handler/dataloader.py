from abc import abstractmethod
from itertools import chain

import numpy as np
import sklearn


__ALL__ = ['BaseDataLoader', 'S2SDataLoader', 'M2MDataLoader', "M2SDataLoader"]


class BaseDataLoader(object):
    def __init__(self, dataset, split_ratio=None):

        if split_ratio is None:
            self._split_ratio = [8,1,1]
        else:
            self._split_ratio = split_ratio

        self._train_size = -1
        self._valid_size = -1
        self._test_size = -1

        self._train_dialog_data = None
        self._valid_dialog_data = None
        self._test_dialog_data = None

        self._train_label_list = []
        self._valid_label_list = []
        self._test_label_list = []


        self._train_tok_dialog_data = None
        self._valid_tok_dialog_data = None
        self._test_tok_dialog_data = None

        self._train_tok_label_list = []
        self._valid_tok_label_list = []
        self._test_tok_label_list = []


        self._dialog_data = dataset.dialog_data
        self._word2id = dataset.word2id
        self._unk_id = dataset.unk_id
        self._pad_id = dataset.pad_id
        self._sos_id = dataset.sos_id
        self._eos_id = dataset.eos_id
        self._label_data = dataset.labels_list
        self._label_name_list = dataset.label_name_list
        self._label2id_list = dataset.label2id_list
        self._data_size = dataset.data_size

        # if self._tokenized:

        self._tok_dialog_data = self.tokenize_dialogs(self._dialog_data)
        self._tok_label_data = self.tokenize_labels(self._label_data)

        self.split_train_valid_test()

    @property
    def train_size(self):
        return self._train_size

    @property
    def valid_size(self):
        return self._valid_size

    @property
    def test_size(self):
        return self._test_size

    @property
    def train_dialog_data(self):
        return self._train_dialog_data

    @property
    def valid_dialog_data(self):
        return self._valid_dialog_data

    @property
    def test_dialog_data(self):
        return self._test_dialog_data

    @property
    def train_label_list(self):
        return self._train_label_list

    @property
    def valid_label_list(self):
        return self._valid_label_list

    @property
    def test_label_list(self):
        return self._test_label_list

    @property
    def train_tok_dialog_data(self):
        return self._train_tok_dialog_data

    @property
    def valid_tok_dialog_data(self):
        return self._valid_tok_dialog_data

    @property
    def test_tok_dialog_data(self):
        return self._test_tok_dialog_data


    @property
    def train_tok_label_list(self):
        return self._train_tok_label_list

    @property
    def valid_tok_label_list(self):
        return self._valid_tok_label_list

    @property
    def test_tok_label_list(self):
        return self._test_tok_label_list

    """
    @property
    def tokenized(self):
        return self._tokenized
    """

    @property
    def split_ratio(self):
        return self._split_ratio

    def shuffle(self):
        outputs = sklearn.utils.shuffle(
            *([self._dialog_data, self._tok_dialog_data] + self._label_data + self._tok_label_data))
        self._dialog_data = outputs[0]
        self._tok_dialog_data = outputs[1]
        self._label_data = outputs[2:len(self._label_data) + 2]
        self._tok_label_data = outputs[len(self._label_data) + 2:]

        """
        if self._tokenized:
            outputs = sklearn.utils.shuffle(
                *([self._dialog_data, self._tok_dialog_data] + self._label_data + self._tok_label_data))
            self._dialog_data = outputs[0]
            self._tok_dialog_data = outputs[1]
            self._label_data = outputs[2:len(self._label_data)+2]
            self._tok_label_data = outputs[len(self._label_data)+2:]
        else:
            outputs = sklearn.utils.shuffle(*([self._dialog_data] + self._label_data))
            self._dialog_data = outputs[0]
            self._label_data = outputs[1:]
        """

    def tokenize_dialogs(self, dialog_data):
        ret = []
        for dial in dialog_data:
            tok_dial = [[self._word2id.get(word, self._unk_id) for word in utt] for utt in dial]
            ret.append(tok_dial)
        return ret

    def tokenize_labels(self, label_data):
        ret = []
        for idx, label2id in enumerate(self._label2id_list):
            cur_data = label_data[idx]
            tok_cur_data = [label2id.get(lab) for lab in cur_data]
            ret.append(tok_cur_data)
        return ret

    def split_train_valid_test(self):

        self.shuffle()

        self._train_size = int(self._data_size * self._split_ratio[0] / np.sum(self._split_ratio))
        self._valid_size = int(self._data_size * self._split_ratio[1] / np.sum(self._split_ratio))
        self._test_size = int(self._data_size * self._split_ratio[2] / np.sum(self._split_ratio))

        self._train_dialog_data = self._dialog_data[:self._train_size]
        self._valid_dialog_data = self._dialog_data[self._train_size:(self._train_size + self._valid_size)]
        self._test_dialog_data = self._dialog_data[(self._train_size + self._valid_size):]


        for labels in self._label_data:
            self._train_label_list.append(labels[:self._train_size])
            self._valid_label_list.append(labels[self._train_size:(self._train_size + self._valid_size)])
            self._test_label_list.append(labels[(self._train_size + self._valid_size):])

        """
        if self._tokenized:
            self._train_tok_dialog_data = self._tok_dialog_data[:self._train_size]
            self._valid_tok_dialog_data = self._tok_dialog_data[self._train_size:(self._train_size + self._valid_size)]
            self._test_tok_dialog_data = self._tok_dialog_data[(self._train_size + self._valid_size):]


            for labels in self._tok_label_data:
                self._train_tok_label_list.append(labels[:self._train_size])
                self._valid_tok_label_list.append(labels[self._train_size:(self._train_size + self._valid_size)])
                self._test_tok_label_list.append(labels[(self._train_size + self._valid_size):])
        """

        self._train_tok_dialog_data = self._tok_dialog_data[:self._train_size]
        self._valid_tok_dialog_data = self._tok_dialog_data[self._train_size:(self._train_size + self._valid_size)]
        self._test_tok_dialog_data = self._tok_dialog_data[(self._train_size + self._valid_size):]

        for labels in self._tok_label_data:
            self._train_tok_label_list.append(labels[:self._train_size])
            self._valid_tok_label_list.append(labels[self._train_size:(self._train_size + self._valid_size)])
            self._test_tok_label_list.append(labels[(self._train_size + self._valid_size):])


    def create_batch_generator(self, dialog_data, batch_size):

        all_lens = [len(dial) for dial in dialog_data]
        indexes = list(np.argsort(all_lens))
        batch_num = int(len(dialog_data) / batch_size)
        print("batch_num: %d" % batch_num)

        batch_indexes = []
        for idx in range(batch_num):
            start_index = idx * batch_size
            end_index = (idx + 1) * batch_size
            batch_indexes.append(indexes[start_index:end_index])

        for b_ids in batch_indexes:
            batch_data = [dialog_data[idx] for idx in b_ids]
            batch_input = self.process_batch_data(batch_data)
            yield batch_input


    @abstractmethod
    def process_batch_data(self, batch_data):
        pass

    def create_train_generator(self, batch_size):
        return self.create_batch_generator(self._train_tok_dialog_data, batch_size)

    def create_test_generator(self, batch_size):
        return self.create_batch_generator(self._test_tok_dialog_data, batch_size)

    def create_valid_generator(self, batch_size):
        return self.create_batch_generator(self._valid_tok_dialog_data, batch_size)


class S2SDataLoader(BaseDataLoader):

    def __init__(self, dataset, max_utt_len, max_dial_size, split_ratio):
        BaseDataLoader.__init__(self, dataset, split_ratio)

        self._max_utt_len = max_utt_len
        self._max_dial_size = max_dial_size

    def process_batch_data(self, batch_data):
        encoder_inputs = []
        encoder_lengths = []
        decoder_inputs = []
        decoder_lengths = []
        decoder_targets = []

        enc_length = (self._max_dial_size - 1) * self._max_utt_len
        dec_length = self._max_utt_len

        for dial in batch_data:
            assert len(dial) >= self._max_dial_size
            dial = dial[:self._max_dial_size]

            context = dial[:-1]
            context = list(chain(*context))[:enc_length]
            context_len = len(context)
            enc_input = context + [self._pad_id] * (enc_length - len(context))

            response = dial[-1][:dec_length]
            dec_len = len(response)
            dec_input = [self._sos_id] + response[:-1] + [self._pad_id] * (dec_length - len(response))
            dec_target = response[1:] + [self._eos_id] + [self._pad_id] * (dec_length - len(response))

            encoder_inputs.append(enc_input)
            encoder_lengths.append(context_len)
            decoder_inputs.append(dec_input)
            decoder_lengths.append(dec_len)
            decoder_targets.append(dec_target)

        return np.array(encoder_inputs), np.array(encoder_lengths), np.array(decoder_inputs), \
               np.array(decoder_lengths), np.array(decoder_targets)



class M2SDataLoader(BaseDataLoader):
    def __init__(self, dataset, max_utt_len, max_dial_size, split_ratio):
        BaseDataLoader.__init__(self, dataset, split_ratio)

        self._max_utt_len = max_utt_len
        self._max_dial_size = max_dial_size

    def process_batch_data(self, batch_data):
        encoder_inputs = []
        encoder_lengths = []
        decoder_inputs = []
        decoder_lengths = []
        decoder_targets = []

        dec_length = self._max_utt_len

        for dial in batch_data:
            assert len(dial) >= self._max_dial_size
            dial = dial[:self._max_dial_size]

            context = dial[:-1]
            enc_utt_input = []
            enc_utt_len = []
            for utt in context:
                utt = utt[:min(len(utt), self._max_utt_len)]
                enc_utt_len.append(len(utt))
                padded_utt = utt + [self._pad_id] * (self._max_utt_len - len(utt))
                enc_utt_input.append(padded_utt)

            response = dial[-1][:dec_length]
            dec_len = len(response)
            dec_input = [self._sos_id] + response[:-1] + [self._pad_id] * (dec_length - len(response))
            dec_target = response[1:dec_length] + [self._eos_id] + [self._pad_id] * (dec_length - len(response))

            encoder_inputs.append(enc_utt_input)
            encoder_lengths.append(enc_utt_len)
            decoder_inputs.append(dec_input)
            decoder_lengths.append(dec_len)
            decoder_targets.append(dec_target)

        return np.array(encoder_inputs), np.array(encoder_lengths), np.array(decoder_inputs), \
               np.array(decoder_lengths), np.array(decoder_targets)



class M2MDataLoader(BaseDataLoader):
    def __init__(self, dataset, max_utt_len, max_dial_size, split_ratio):
        BaseDataLoader.__init__(self, dataset, split_ratio)

        self._max_utt_len = max_utt_len
        self._max_dial_size = max_dial_size

    def process_batch_data(self, batch_data):
        pass














"""


class KGCVAEDataLoader(BaseDataLoader):

    def __init__(self, config, cleaned_texts, label_list, word2id, id2word, label2id_list, id2label_list,
                 label_name_list, acts, act2id, id2act):
        self._acts = acts
        self._act2id = act2id
        self._id2act = id2act
        self._acts = self._tokenize_acts(self._acts)
        super().__init__(config, cleaned_texts, label_list, word2id, id2word, label2id_list, id2label_list,
                         label_name_list)
        self._split_acts()

    def _shuffle_data(self):
        if len(self._label_list) != 0:
            output = sklearn.utils.shuffle(*([self._dialog_data] + [self._acts] + self._label_list))
            self._dialog_data = output[0]
            self._acts = output[1]
            self._label_list = output[2:]
        else:
            output = sklearn.utils.shuffle(*([self._dialog_data] + [self._acts] + self._label_list))
            self._dialog_data = output[0]
            self._acts = output[1]

    def get_generator(self, dialog_data, label_list):
        if len(label_list) != 0:
            assert len(dialog_data) == len(label_list[0])
        def generate():
            all_lens = [len(dial) for dial in dialog_data]  # [2,3,4,2]
            indexes = list(np.argsort(all_lens))  # [2,1,0,3]
            batch_num = int(len(dialog_data) / self._batch_size)

            batch_indexes = []
            for idx in range(batch_num):
                start_index = idx * self._batch_size
                end_index = (idx + 1) * self._batch_size
                batch_indexes.append(indexes[start_index:end_index])  # [2,1][0,3]

            for b_ids in batch_indexes:
                batch_data = [dialog_data[idx] for idx in b_ids]
                batch_acts = [self._acts[idx] for idx in b_ids]
                batch_labels = []
                for labels in label_list:
                    batch_labels.append([labels[idx] for idx in b_ids])

                batch_input = self._create_batch(batch_data, batch_labels, batch_acts)
                yield batch_input
        return generate

    def _create_batch(self, batch_data, batch_labels, batch_acts):
        encoder_inputs = []
        encoder_lengths = []
        decoder_inputs = []
        decoder_lengths = []
        decoder_targets = []
        acts = []
        floors = []

        dec_length = self._max_utterance_length
        assert "topic" in self._label_name_list
        label_idx = self._label_name_list.index("topic")
        topics = batch_labels[label_idx]

        for i in range(len(batch_data)):

            dial = batch_data[i]
            assert len(dial) >= self._max_dialog_size
            dial = dial[:self._max_dialog_size]

            context = dial[:-1]
            enc_input = []
            context_len = []
            floor = [0, 1] * len(context)
            floor = floor[:len(context)]
            for utt in context:
                utt = utt[:min(len(utt), self._max_utterance_length)]
                context_len.append(len(utt))
                padded_utt = utt + [self._pad_id] * (self._max_utterance_length - len(utt))
                enc_input.append(padded_utt)

            response = dial[-1][:(dec_length - 1)]
            dec_len = len(response) + 1
            dec_input = [self._sos_id] + response + [self._pad_id] * (dec_length - 1 - len(response))
            dec_target = response[:(dec_length - 1)] + [self._eos_id] + [self._pad_id] * (
                    dec_length - 1 - len(response))

            encoder_inputs.append(enc_input)
            encoder_lengths.append(context_len)
            decoder_inputs.append(dec_input)
            decoder_lengths.append(dec_len)
            decoder_targets.append(dec_target)
            acts.append(batch_acts[i][self._max_dialog_size-1])
            floors.append(floor)

        return [np.array(encoder_inputs), np.array(encoder_lengths), np.array(decoder_inputs),
                np.array(decoder_lengths), np.array(decoder_targets), np.array(topics),
                np.array(acts), np.array(floors)]

    def _tokenize_acts(self, acts):
        tokenized_acts = [[self._act2id.get(act)
                           for act in dialog] for dialog in acts]
        return tokenized_acts

    def _split_acts(self):

        self._train_acts = self._acts[:self._train_valid_split]
        self._valid_acts = self._acts[self._train_valid_split:self._valid_test_split]
        self._test_acts = self._acts[self._valid_test_split:]

"""