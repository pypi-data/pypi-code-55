# -*- coding: utf-8 -*-

from fastai.text import *
from pytorch_pretrained_bert import BertTokenizer
from pytorch_pretrained_bert.modeling import BertModel
from pytorch_pretrained_bert.modeling import BertPreTrainedModel

class MyExtractor(BertPreTrainedModel):
  def __init__(self, config, lstm_feature_size):
    super().__init__(config)  # 模型结构：==> BertModel => Dropout => LSTM ==>
    self.bert, self.drop = BertModel(config), nn.Dropout(config.hidden_dropout_prob)
    # for p in self.bert.parameters(): p.requires_grad = False  # 冻结bert参数
    self.lstm = nn.LSTM(config.hidden_size, lstm_feature_size, 2, batch_first=True)
    self.apply(self.init_bert_weights)  # 加载由from_pretrained函数指定的预训练模型

  def forward(self, data):
    # BertModel每一层都可以作为句向量使用
    bert_output = self.bert(data)[0][-1]
    drop_output = self.drop(bert_output)
    lstm_output = self.lstm(drop_output)
    _, (lstm_output, __) = lstm_output
    return self.drop(lstm_output[-1])

# 加载多语言区分大小写版本的BertPreTrainedModel，注意需要与BertTokenizer保持一致
myExtractor = MyExtractor.from_pretrained('bert-base-multilingual-cased', 512)
myModel = nn.Sequential(myExtractor, nn.Linear(512, 128), nn.Linear(128, 2))

def predict(model_path, model_file, data_list):
    myLearner = load_learner(model_path, model_file)
    myLearner.data.add_test(data_list)
    preds, _ = myLearner.get_preds(ds_type=DatasetType.Test)
    return [float(x[1]) for x in preds]