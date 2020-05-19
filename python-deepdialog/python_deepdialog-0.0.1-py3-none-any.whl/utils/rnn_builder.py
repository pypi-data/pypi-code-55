import tensorflow as tf

__ALL__ = ['create_rnn_cell']


def create_rnn_cell(cell_type, hidden_units, num_layers, input_keep_prob=1.0, output_keep_prob=1.0, use_residual=False):
    """
    Utilities for creating RNN cell.

    Parameters
    ----------
    cell_type: string
        The type of RNN cell. could be either `lstm` or `gru`.
    hidden_units: integer
        The number of hidden units.
    num_layers: integer
        The number of layers of RNN.
    """
    def _new_cell():
        if cell_type == "lstm":
            return tf.contrib.rnn.LSTMCell(hidden_units)
        elif cell_type == "gru":
            return tf.contrib.rnn.GRUCell(hidden_units)
        else:
            raise ValueError("cell_type must be either lstm or gru")

    def _new_wrapper_cell(residual_connection=False):
        cell = _new_cell()
        if input_keep_prob < 1.0 or output_keep_prob < 1.0:
            cell = tf.contrib.rnn.DropoutWrapper(cell,
                                                 input_keep_prob=input_keep_prob, output_keep_prob=output_keep_prob)
        if residual_connection:
            cell = tf.contrib.rnn.ResidualWrapper(cell)
        return cell

    if num_layers > 1:
        cells = []
        for i in range(num_layers):
            is_residual = True if use_residual and i > 1 else False
            cells.append(_new_wrapper_cell(is_residual))
        return tf.contrib.rnn.MultiRNNCell(cells)
    else:
        return _new_wrapper_cell(residual_connection=False)
