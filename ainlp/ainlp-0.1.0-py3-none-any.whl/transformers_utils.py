from abc import ABC, abstractmethod
from attrdict import AttrDict
from ainlp import QATokenizer
import os.path
import hashlib
import torch
import numpy as np
import random
import logging
from torch.optim.lr_scheduler import LambdaLR
from tqdm.autonotebook import tqdm, trange

logger = logging.getLogger(__name__)


class BaseProcessor(ABC):
    def __init__(self, tokenizer, max_length=180, max_query_length=60,
                 batch_size=48, shuffle=True, doc_stride=32, drop_last=True, **kwargs):
        self.tokenizer = QATokenizer(tokenizer)
        self.max_length = max_length
        self.max_query_length = max_query_length
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.doc_stride = doc_stride
        self.drop_last = drop_last

    @abstractmethod
    def create_example(self, example_id, item, **kwargs):
        """创建Example对象
        Example对象代表每一条标注样本
        :param example_id: example id
        :param item: data item
        :param kwargs:
        :return: AttrDict object representing an example.
        """
        pass

    @abstractmethod
    def create_training_features(self, example):
        """从Example创建模型训练输入数据Features
        一个Example对象可能返回多个Features，比如QA问题，当context text超过模型允许的max_length时，需要采用滑动窗口技术返回
        多个Features，从多个Features的预测结果中选取最好的结果
        :param example: AttrDict object
        :return: list of AttrDict objects
        """
        pass

    @abstractmethod
    def create_evaluation_features(self, example):
        """从Example创建模型评估输入数据Features
        一般create_training_features与create_evaluation_features方法会有些许不同逻辑
        :param example: AttrDict object
        :return: list of AttrDict objects
        """
        pass

    @abstractmethod
    def create_dataset(self, examples, features, is_training=True, **kwargs):
        """创建Dataset
        :param examples: list of examples
        :param features: list of features
        :param is_training:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def get_examples(self, data_path, **kwargs):
        """从数据文件中读取每条记录item，然后调用create_example创建Example对象
        :param data_path:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def print_feature(self, feature):
        """打印feature变量
        调试用
        :param feature:
        :return:
        """
        pass

    def _get_cache_path(self, data_path, cache_dir=None):
        """create cache path according to data_path
        :param data_path: data file path
        :param cache_dir: cache directory, default use the same directory with data_path
        :return: file name named after 'cached_{md5}'
        """
        data_dir = os.path.dirname(data_path) if cache_dir is None else cache_dir
        m = hashlib.md5()
        m.update(data_path.encode('utf8'))
        return os.path.join(data_dir, 'cached_{}'.format(m.hexdigest()))

    def load_and_cache(self, data_path, is_training=True, output_examples=False, overwrite_cache=False,
                       debug=False, cache_dir=None, **kwargs):
        """加载数据文件，返回DataLoader对象
        :param data_path: data file path
        :param is_training: training or evaluation
        :param output_examples: if True, return examples and features
        :param overwrite_cache: if True, ignore local cache
        :param debug: if True, print first 10 features
        :param kwargs: other keyword parameters which will be passed to get_examples, create_dataset
        :param cache_dir: cache directory
        :return: loader, (examples, features)
        """
        # use cache
        cache_path = self._get_cache_path(data_path, cache_dir)
        if not overwrite_cache and os.path.exists(cache_path):
            cache_data = torch.load(cache_path)
            loader, examples, features = cache_data['loader'], cache_data['examples'], cache_data['features']
            if output_examples:
                return loader, examples, features
            return loader

        # no cache
        examples = self.get_examples(data_path, **kwargs)
        features = []
        for example in tqdm(examples, desc='Creating Features'):
            if is_training:
                features += self.create_training_features(example)
            else:
                features += self.create_evaluation_features(example)
        # print first 10 features
        if debug:
            for f in features[:10]:
                self.print_feature(f)

        dataset = self.create_dataset(examples, features, is_training, **kwargs)
        loader = torch.utils.data.DataLoader(
            dataset, shuffle=self.shuffle, batch_size=self.batch_size, drop_last=True
        )
        # save to cache
        if cache_dir and not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        torch.save({'loader': loader, 'examples': examples, 'features': features}, cache_path)
        if output_examples:
            return loader, examples, features
        return loader


class BaseModeler(object):
    def __init__(self, model, **kwargs):
        self.model = model
        self.kwargs = kwargs

    def _update_kwargs(self, **kwargs):
        copy = self.kwargs.copy()
        copy.update(kwargs)
        return copy

    def create_optimizer(self, **kwargs):
        kwargs = self._update_kwargs(**kwargs)
        weight_decay = kwargs.get('weight_decay', 0.01)
        learning_rate = kwargs.get('learning_rate', 3e-5)
        adam_epsilon = kwargs.get('adam_epsilon', 1e-6)
        no_decay = ['bias', 'LayerNorm.weight']
        grouped_parameters = [
            {
                'params': [p for n, p in self.model.named_parameters()
                           if not any(nd in n for nd in no_decay)],
                'weight_decay': weight_decay
            },
            {
                'params': [p for n, p in self.model.named_parameters()
                           if any(nd in n for nd in no_decay)],
                'weight_decay': 0.0
            }
        ]
        optimizer = torch.optim.AdamW(grouped_parameters, lr=learning_rate, eps=adam_epsilon)
        return optimizer

    def create_scheduler(self, optimizer, **kwargs):
        kwargs = self._update_kwargs(**kwargs)
        num_warmup_steps = kwargs.get('num_warmup_steps')
        num_training_steps = kwargs.get('num_training_steps')
        last_epoch = kwargs.get('last_epoch', -1)

        def lr_lambda(current_step):
            if current_step < num_warmup_steps:
                return float(current_step) / float(max(1, num_warmup_steps))
            return max(
                0.0, float(num_training_steps - current_step) / float(max(1, num_training_steps - num_warmup_steps))
            )

        return LambdaLR(optimizer, lr_lambda, last_epoch)

    @abstractmethod
    def train_batch(self, batch):
        """输入batch， 返回模型训练结果
        :param batch: DataLoader返回的batch
        :return: outputs. list, whose first element must be loss
        """
        self.model.train()
        batch = tuple(t.to(self.model.device) for t in batch)
        return self.model(*batch)

    @abstractmethod
    def predict_batch(self, batch):
        """输入batch，返回模型预测结果
        :param batch:
        :return: outputs, list
        """
        self.model.eval()
        batch = tuple(t.to(self.model.device) for t in batch)
        with torch.no_grad():
            outputs = self.model(*batch)
            return outputs

    def set_seed(self, seed):
        """设置随机数种子，可以保证运行结果可以复现
        :param seed:
        :return:
        """
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

    def train(self, output_dir, data_loader, num_epochs, **kwargs):
        optimizer = self.create_optimizer(**kwargs)
        num_training_steps = len(data_loader) * num_epochs
        scheduler = self.create_scheduler(optimizer, num_warmup_steps=int(num_training_steps * 0.06),
                                          num_training_steps=num_training_steps, **kwargs)

        kwargs = self._update_kwargs(**kwargs)
        logging_steps = kwargs.get('logging_steps', 500)
        save_steps = kwargs.get('save_steps', 500)
        seed = kwargs.get('seed', 100)
        tb_writer = torch.utils.tensorboard.SummaryWriter()

        # added here for reproducibility
        self.set_seed(seed)
        self.model.zero_grad()
        global_step = 0
        tr_loss, logging_loss = 0.0, 0.0
        for _ in trange(num_epochs):
            epoch_iterator = tqdm(data_loader, desc='Iteration')
            for step, batch in enumerate(epoch_iterator):
                outputs = self.train_batch(batch)
                loss = outputs[0]
                loss.backward()

                tr_loss += loss.item()
                # TODO: why clip gradients
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                optimizer.step()  # update weights
                scheduler.step()  # update learning rate

                self.model.zero_grad()  # zero gradients
                global_step += 1

                if logging_steps > 0 and global_step % logging_steps == 0:
                    tb_writer.add_scalar('lr', scheduler.get_lr()[0], global_step)
                    tb_writer.add_scalar('loss', (tr_loss - logging_loss) / logging_steps, global_step)
                    logging_loss = tr_loss

                if save_steps > 0 and global_step % save_steps == 0:
                    output_ckp_dir = os.path.join(output_dir, 'checkpoint-{}'.format(global_step))
                    if not os.path.exists(output_ckp_dir):
                        os.makedirs(output_ckp_dir)
                    self.model.save_pretrained(output_ckp_dir)
                    torch.save(optimizer.state_dict(), os.path.join(output_ckp_dir, 'optimizer.pt'))
                    torch.save(scheduler.state_dict(), os.path.join(output_ckp_dir, 'scheduler.pt'))
                    logger.info('Saveing optimizer and scheduler states to %s', output_ckp_dir)
        tb_writer.close()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.model.save_pretrained(output_dir)
        return global_step, tr_loss / global_step

    @abstractmethod
    def evaluate(self, data_loader, examples, features, **kwargs):
        """ 评估模型效果，输出DataFrame结果以供指标评估 """
        pass

    @abstractmethod
    def predict(self, examples, features, data_loader=None, **kwargs):
        """ 预测结果，输出DataFrame结果以供预览，用于批量预测
        :param examples: list of Examples
        :param features: list of Features respective to Examples
        :param data_loader: optional, if specified, use data_loader to batch predict, otherwise
            construct one batch data_loader to predict examples
        :param kwargs:
        """
        pass

    def predict_items(self, items, processor, **kwargs):
        """ 预测结果，输出DataFrame结果以供指标评估，用于在线预测
        :param items:
        :param processor:
        :param kwargs:
        :return:
        """
        examples = [processor.create_example(i, item, **kwargs) for i, item in enumerate(items)]
        features = []
        for example in examples:
            features += processor.create_evaluation_features(example)
        return self.predict(examples, features, **kwargs)
