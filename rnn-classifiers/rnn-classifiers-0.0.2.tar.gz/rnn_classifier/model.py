"""model.py
Author: Urchade Zaratiana
"""

from torch import nn


class RNNClassifier(nn.Module):
    def __init__(self, input_size, hidden_units=128, num_classes=1, num_classifier_layers=2, rnn_hidden_size=64,
                 rnn_type='lstm', num_rnn_layers=1, bidirectional=False, batch_first=True, activation=nn.ReLU()):
        super().__init__()

        self.rnn_type = rnn_type
        direction = 2 if bidirectional else 1

        configs = {'input_size': input_size, 'hidden_size': rnn_hidden_size, 'num_layers': num_rnn_layers,
                   'bidirectional': bidirectional, 'batch_first': batch_first}

        rnn_dict = {'lstm': nn.LSTM(**configs),
                    'gru': nn.GRU(**configs),
                    'simple': nn.RNN(**configs)}

        self.rnn_layer = rnn_dict[rnn_type]

        self.out_rnn = num_rnn_layers * direction * rnn_hidden_size

        intermediate = self.out_rnn

        classifier = []

        for i in range(num_classifier_layers):
            classifier.append(nn.Linear(intermediate, hidden_units))
            classifier.append(activation)
            intermediate = hidden_units

        classifier.append(nn.Linear(hidden_units, num_classes))

        self.fully_connected = nn.Sequential(*classifier)

    def forward(self, x):

        if self.rnn_type == 'lstm':
            _, (h, _) = self.rnn_layer(x)
        else:
            _, h = self.rnn_layer(x)

        h = h.view(-1, self.out_rnn)

        return self.fully_connected(h)