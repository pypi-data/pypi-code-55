from soco_encoders.cloud_bucket import CloudBucket
from soco_encoders.encoders import *
from soco_encoders.Tokenizer import Tokenizer
from soco_encoders.util import Pack


class EncoderLoader(object):

    @staticmethod
    def _load_sent_transformer(config, model_family, model_id, use_gpu, region):
        bucket = CloudBucket(region)
        model_dir = bucket.download_transformer_model(model_family, model_id)

        constructor = globals()[config.encoder_class]
        model = constructor(model_dir, config)
        model.eval()
        if use_gpu:
            model.cuda()

        return model

    @staticmethod
    def _load_term_transformer(config, model_family, model_id, use_gpu, region):
        bucket = CloudBucket(region)
        model_dir = bucket.download_term_transformer_model(model_family, model_id)

        constructor = globals()[config.encoder_class]
        model = constructor(model_dir, config)
        model.eval()
        if use_gpu:
            model.cuda()

        return model

    @staticmethod
    def load_model(model_family, model_id, use_gpu, region='us'):
        if not torch.cuda.is_available():
            use_gpu = False

        bucket = CloudBucket(region)
        model_dir = bucket.download_config(model_family, model_id)
        config = json.load(open(os.path.join(model_dir, 'config.json')))
        config['use_gpu'] = use_gpu
        config = Pack(config)
        if config.encoder_class == 'TransformerWrapper':
            return EncoderLoader._load_sent_transformer(config, model_family, model_id, use_gpu, region)
        elif config.encoder_class == 'TermTransformer':
            return EncoderLoader._load_term_transformer(config, model_family, model_id, use_gpu, region)

        else:
            raise Exception("{} is unknown.".format(config.encoder_class))

    @staticmethod
    def load_tokenizer(model_id, region='us'):
        return Tokenizer(model_id, region)

