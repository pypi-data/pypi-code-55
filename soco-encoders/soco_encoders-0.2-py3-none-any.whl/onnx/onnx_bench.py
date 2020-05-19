import torch
from temp_model import TermQAModel
import json
import os
from soco_encoders.utils import Pack
import time


model_dir = 'resources/bert-base-uncase-ti-log-320head-s_n'
config = json.load(open(os.path.join(model_dir, 'config.json')))
config['use_gpu'] = torch.cuda.is_available()
config = Pack(config)
model = TermQAModel(model_dir, config)
model.eval()
q_batch_size = 1000
a_batch_size = 10
q_ids = torch.arange(1000, 1000+q_batch_size).long().view(q_batch_size, 1)
a_input_ids = torch.ones(a_batch_size, 320).long() * 1233
a_attention_mask = torch.ones(a_batch_size, 320).long()
a_token_type_ids = torch.ones(a_batch_size, 320).long()


inputs = {
    'q_ids': q_ids,
    'a_input_ids': a_input_ids,
    'a_attention_mask': a_attention_mask,
    'a_token_type_ids': a_token_type_ids
}

output_model_path = './bert-base-uncase-ti-log-320head-s_n.onnx'
outputs = {}

with torch.no_grad():
    inputs = {k: v.to('cuda') if config.use_gpu else v for k, v in inputs.items()}
    start = time.time()
    model(**inputs)
    end = time.time()
    print("PyTorch Inference time = ", end - start)

import onnxruntime as rt

sess_options = rt.SessionOptions()

# Set graph optimization level to ORT_ENABLE_EXTENDED to enable bert optimization.
sess_options.graph_optimization_level = rt.GraphOptimizationLevel.ORT_ENABLE_EXTENDED
sess_options.intra_op_num_threads=8

# To enable model serialization and store the optimized graph to desired location.
sess_options.optimized_model_filepath = os.path.join('pytorch_output',
                                                     "optimized_bert-base-uncase-ti-log-320head-s_n.onnx")
session = rt.InferenceSession(output_model_path, sess_options)

# evaluate the model
rt_input =  {
    'q_ids': inputs['q_ids'].cpu().numpy(),
    'a_input_ids': inputs['a_input_ids'].cpu().numpy(),
    'a_attention_mask': inputs['a_attention_mask'].cpu().numpy(),
    'a_token_type_ids': inputs['a_token_type_ids'].cpu().numpy()
}
start = time.time()
res = session.run(None, rt_input)
end = time.time()
print("ONNX Runtime inference time: ", end - start)