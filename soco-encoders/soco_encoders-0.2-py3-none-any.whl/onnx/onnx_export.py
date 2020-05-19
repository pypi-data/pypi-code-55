import torch
from temp_model import TermQAModel
import json
import os
from soco_encoders.utils import Pack
import time
import onnxmltools
from onnxmltools.utils.float16_converter import convert_float_to_float16

model_dir = 'resources/bert-base-uncase-ti-log-320head-s_n'
config = json.load(open(os.path.join(model_dir, 'config.json')))
config['use_gpu'] = torch.cuda.is_available()
config = Pack(config)
model = TermQAModel(model_dir, config)
model.eval()
q_batch_size = 1000
a_batch_size = 1
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

inputs = {k: v.to('cuda') if config.use_gpu else v for k, v in inputs.items()}
output_model_path = './bert-base-uncase-ti-log-320head-s_n.onnx'
half_output_model_path = './bert-base-uncase-ti-log-320head-s_n.16.onnx'

start = time.time()
outputs = model(**inputs)
end = time.time()
print("PyTorch Inference time = ", end - start)

with torch.no_grad():
    q_names = {0: 'q_batch_size', 1: 'max_q_len'}
    a_names = {0: 'a_batch_size'}
    qa_names = {0: 'q_batch_size', 1: 'a_batch_size'}

    torch.onnx.export(model,  # model being run
                      (inputs['q_ids'],
                       inputs['a_input_ids'],  # model input (or a tuple for multiple inputs)
                       inputs['a_attention_mask'],
                       inputs['a_token_type_ids']),
                      output_model_path,  # where to save the model (can be a file or file-like object)
                      opset_version=11,  # the ONNX version to export the model to
                      do_constant_folding=True,  # whether to execute constant folding for optimization
                      input_names=['q_ids',
                                   'a_input_ids',  # the model's input names
                                   'a_attention_mask',
                                   'a_token_type_ids'],
                      output_names=['scores'],  # the model's output names
                      dynamic_axes={'q_ids': q_names,
                                    'a_input_ids': a_names,  # variable length axes
                                    'a_attention_mask': a_names,
                                    'a_token_type_ids': a_names,
                                    'scores': qa_names})
    print("Model exported at ", output_model_path)

onnx_model = onnxmltools.utils.load_model(output_model_path)
onnx_model = convert_float_to_float16(onnx_model)
onnxmltools.utils.save_model(onnx_model, half_output_model_path)
