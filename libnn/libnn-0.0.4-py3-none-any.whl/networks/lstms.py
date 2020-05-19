import torch
import torch.nn as nn
import torch.nn.functional as F

class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size = 7):
        super().__init__()
        self.lstm = torch.nn.LSTM(
            input_size = input_size,
            hidden_size = hidden_size,
            num_layers = 3,
            batch_first = True,
            dropout = 0.2
        )
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, 64),
            nn.Linear(64, output_size)
        )
        # self.out = torch.nn.Linear(in_features=hidden_size, out_features=1)


    def forward(self, x):
        # 一下关于shape的注释只针对单项
        # output: [batch_size, time_step, hidden_size]
        # h_n: [num_layers,batch_size, hidden_size] # 虽然LSTM的batch_first为True,但是h_n/c_n的第一维还是num_layers
        # c_n: 同h_n
        output, (h_n, c_n) = self.lstm(x)
        # print(output.size())
        # output_in_last_timestep=output[:,-1,:] # 也是可以的
        output_in_last_timestep = h_n[-1, :, :]
        # print(output_in_last_timestep.equal(output[:,-1,:])) #ture
        # x = self.out(output_in_last_timestep)
        x = self.fc(output_in_last_timestep)
        return x


# http://chandlerzuo.github.io/blog/2017/11/darnn
