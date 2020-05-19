import boto3
import oss2
import os
import time


class CloudBucket(object):
    roles = {'reader-s3': ('AKIAIXQ4BV6ORFZ3JKPA', 'D+9W2Zii2Hvpo6G0IJ77tofKUM59ZasC/HE3Kf/w'),
             'full-s3': ('AKIAIRZZT5BICC5NFNOA', 'HB2ixc2F12xaFEuqN1G7HwP4VvfgB+l/kgxNXLFd'),
             'reader-oss': ('LTAINYtHd5knNlAg', 'HIg89gNwNYpbEKoC38SdnYCn3Db8cI'),
             'full-oss': ('LTAIkryioiCP2Wn9', 'cutsfNk7rY05qhBVNikYkxny8I4UkK')}

    def __init__(self, region='us', permission='reader'):
        self.region = region.lower()
        self.permission = permission.lower()
        if permission == 'reader':
            s3_key = self.roles['reader-s3']
            oss_key = self.roles['reader-oss']
        elif permission == 'full':
            s3_key = self.roles['full-s3']
            oss_key = self.roles['full-oss']
        else:
            raise Exception("Unknown permission {}".format(permission))
        self._s3 = boto3.resource('s3', aws_access_key_id=s3_key[0], aws_secret_access_key=s3_key[1])
        self._s3_bucket = self._s3.Bucket('convmind-models')
        self._oss_bucket = oss2.Bucket(oss2.Auth(oss_key[0], oss_key[1]),
                                       str('http://oss-accelerate.aliyuncs.com'), str('convmind-models'))

    def safe_mkdir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def download(self, folder_dir, files, local_dir):
        start = time.time()
        for f in files:
            src = '{}/{}'.format(folder_dir, f)
            dest =  os.path.join(local_dir, f)
            try:
                if self.region.lower() == 'cn':
                    self._oss_bucket.get_object_to_file(src, dest)
                else:
                    self._s3_bucket.download_file(src, dest)
            except Exception as e:
                print(e)
                print("Failed to download {}".format(src))

        end = time.time()
        print(("download models using {:.4f} sec".format(end - start)))

    def download_dir(self, folder_dir, dirs, local_dir):
        start = time.time()
        for d in dirs:
            cur_remote_dir = os.path.join(folder_dir, d)
            cur_local_dir = os.path.join(local_dir, d)

            if not os.path.exists(cur_local_dir):
                os.mkdir(cur_local_dir)

            files = []
            if self.region.lower() == 'cn':
                for o in self._oss_bucket.list_objects(prefix=cur_remote_dir).object_list:
                    f_name = o.key.split('/')[-1]
                    if f_name != '':
                        files.append(o.key.split('/')[-1])
            else:
                for o in self._s3_bucket.objects.filter(Prefix=cur_remote_dir):
                    f_name = o.key.split('/')[-1]
                    if f_name != '':
                        files.append(o.key.split('/')[-1])

            self.download(cur_remote_dir, files, cur_local_dir)

        end = time.time()
        print(("download models using {:.4f} sec".format(end - start)))

    def download_config(self, asset_dir, asset_id, local_dir='resources'):
        self.safe_mkdir(local_dir)

        files = ['config.json']
        model_dir = '{}/{}'.format(local_dir, asset_id)
        if not os.path.exists(model_dir):
            self.safe_mkdir(model_dir)

            self.download('{}/{}'.format(asset_dir, asset_id), files, 'resources/{}'.format(asset_id))
        else:
            print("Download is canceled since the asset already exists.")

        return model_dir

    def download_model(self, asset_dir, asset_id, local_dir='resources'):
        self.safe_mkdir(local_dir)

        files = ['m.model', 'm.vocab', 'model', 'params.json']
        model_dir = '{}/{}'.format(local_dir, asset_id)
        if not os.path.exists(os.path.join(model_dir, files[0])):
            self.safe_mkdir(model_dir)
            self.download('{}/{}'.format(asset_dir, asset_id), files, 'resources/{}'.format(asset_id))
        else:
            print("Download is canceled since the asset already exists.")

        return model_dir

    def download_transformer_model(self, asset_dir, asset_id, local_dir='resources'):
        self.safe_mkdir(local_dir)

        files = ['modules.json']
        dirs = ['0_BERT', '1_Pooling']

        model_dir = '{}/{}'.format(local_dir, asset_id)
        if not os.path.exists(os.path.join(model_dir, files[0])):
            self.safe_mkdir(model_dir)

            self.download('{}/{}'.format(asset_dir, asset_id), files, 'resources/{}'.format(asset_id))
            self.download_dir('{}/{}'.format(asset_dir, asset_id), dirs, 'resources/{}'.format(asset_id))
        else:
            print("Download is canceled since the asset already exists.")

        return model_dir

    def download_term_transformer_model(self, asset_dir, asset_id, local_dir='resources'):
        self.safe_mkdir(local_dir)

        files = ['modules.json', 'term_embeddings.bin', 'term_vocab.json']
        dirs = ['0_BERT', '1_Pooling']

        model_dir = '{}/{}'.format(local_dir, asset_id)
        if not os.path.exists(os.path.join(model_dir, files[0])):
            self.safe_mkdir(model_dir)

            self.download('{}/{}'.format(asset_dir, asset_id), files, 'resources/{}'.format(asset_id))
            self.download_dir('{}/{}'.format(asset_dir, asset_id), dirs, 'resources/{}'.format(asset_id))
        else:
            print("Download is canceled since the asset already exists.")

        return model_dir

    def download_tokenizer(self, asset_dir, asset_id, local_dir="resources"):
        self.safe_mkdir(local_dir)
        files = ['vocab.txt', '{}.txt'.format(asset_id), '{}.json'.format(asset_id), 'config.json']
        model_dir = '{}/{}'.format(local_dir, asset_id)
        if not os.path.exists(os.path.join(model_dir, files[0])):
            self.safe_mkdir(model_dir)
            self.download('{}/{}'.format(asset_dir, asset_id), files, 'resources/{}'.format(asset_id))
        else:
            print("Download is canceled since the asset already exists.")

        return model_dir



if __name__ == '__main__':
    b = CloudBucket('us')
    b.download_tokenizer('tokenizers', 'bert-base-chinese')