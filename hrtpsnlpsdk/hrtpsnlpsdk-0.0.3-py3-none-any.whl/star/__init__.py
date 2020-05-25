from typing import List

from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport

from .thriftio import STARService
from ..utils.text_utils import min_len_sen_tokenizer


class STARDetecter(object):

    def __init__(self, host="115.159.102.194", port=16113):
        """
        调用 WEB API
        115.159.102.194 是测试服务器
        """
        self.host = host
        self.port = port

    @classmethod
    def _predict_sen(cls, sub_sen_text, client):
        sub_pre_label = client.star_detect(sub_sen_text)
        return sub_pre_label

    def predict_doc(self, doc_text: str, sen_split="。!?！？：；;:", min_sen_len=64):
        """

        :param doc_text: 长文本
        :param sen_split:  切分句子分隔符
        :param min_sen_len:  长句子切分窗口， 单句子过长则按照此长度平均切分
        :return:
        """
        transport = TSocket.TSocket(self.host, self.port)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)

        thrift_client = STARService.Client(protocol)
        transport.open()

        sub_sens = min_len_sen_tokenizer(doc_text, split_set=sen_split, minlen=min_sen_len)

        for sub_sen in sub_sens:
            sub_sen_text, sub_sen_ind, sub_sen_len = sub_sen
            sub_sen_text = "".join(sub_sen_text)
            sub_pre_label = self._predict_sen(sub_sen_text, thrift_client)
            yield sub_pre_label, sub_sen_text, sub_sen_ind, sub_sen_len
        transport.close()

    def predict_position(self, texts: List, **kwargs) -> List:
        """
        :return:
                [
                    {
                        "tag":[
                            {
                                "name":"句子类型",
                                "offset":"",
                                "length":""
                            }
                        ]
                    }
                ]
        :param texts:
        """
        pre_result = []
        for text in texts:
            tags = []
            # 行文本切分后预测
            for p in self.predict_doc(text, kwargs):
                sub_pre_label, sub_sen_text, sub_sen_ind, sub_sen_len = p
                tags.append({
                    "name": f"{sub_pre_label}",
                    "offset": sub_sen_ind,
                    "length": sub_sen_len,
                })
            pre_result.append({"tag": tags})
        return pre_result




