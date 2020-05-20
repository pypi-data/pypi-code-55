import tensorflow as tf

__ALL__ = ['create_attention']


def create_attention(attention_type, hidden_units, memory, memory_lengths):
    """
    Utilities for creating attention.

    Parameters
    ----------
    attention_type: string
        The type of attention. Currently for types are provided: [`luong`, `scaled_luong`, `bahdanau`,
        `normed_bahdanau`].
    hidden_units: integer
        The number of hidden dimensions.
    memory: a Tensor
        The inputs to be memorized.
    memory_lengths: a Tensor
        The memory lengths.
    """
    if attention_type == "luong":
        attention_mechanism = tf.contrib.seq2seq.LuongAttention(hidden_units, memory,
                                                                memory_sequence_length=memory_lengths)
    elif attention_type == "scaled_luong":
        attention_mechanism = tf.contrib.seq2seq.LuongAttention(hidden_units, memory,
                                                                memory_sequence_length=memory_lengths, scale=True)
    elif attention_type == "bahdanau":
        attention_mechanism = tf.contrib.seq2seq.BahdanauAttention(hidden_units, memory,
                                                                   memory_sequence_length=memory_lengths)
    elif attention_type == "normed_bahdanau":
        attention_mechanism = tf.contrib.seq2seq.BahdanauAttention(hidden_units, memory,
                                                                   memory_sequence_length=memory_lengths, normalize=True)
    else:
        raise ValueError("Unknown attention_type: %s" % attention_type)

    return attention_mechanism
