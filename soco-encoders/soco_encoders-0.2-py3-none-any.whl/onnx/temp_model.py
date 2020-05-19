import torch
import os
import logging
from soco_sentence_transformers import SentenceTransformer


class TermQAModel(torch.nn.Module):
    logger = logging.getLogger(__name__)

    def __init__(self, model_dir, config):
        super(TermQAModel, self).__init__()
        self.term_embedding = torch.load(os.path.join(model_dir, 'term_embeddings.bin'))
        self.a_bert = SentenceTransformer(model_dir, device='cuda' if config.use_gpu else 'cpu')
        self.device = "cuda" if torch.cuda.is_available() and config.use_gpu else "cpu"

        if config.use_gpu:
            self.logger.info("Use pytorch device: {}".format(self.device))
            self.term_embedding.to(self.device)

    def _multi_head_cross_similarity(self, q_feature, c_feature):
        """
        :param q_feature: query_size x T x hidden_size
        :param c_feature: doc_size x num_head x hidden_size
        :param q_mask: query_size x T
        :return:
        """
        Q = q_feature.shape[0]
        T = q_feature.shape[1]
        H = q_feature.shape[2]
        A = c_feature.shape[0]
        N = c_feature.shape[1]

        flat_c_feature = c_feature.view(-1, H) # (A x N) x H
        flat_q_feature = q_feature.view(-1, H) # (Q x T) x H

        head_logits = torch.matmul(flat_q_feature, flat_c_feature.transpose(0, 1))
        logits = head_logits.view(-1, A, N)  # (QxT) x A x N

        probs = torch.softmax(logits, dim=2).unsqueeze(2)  # (QxT)x A x 1 x N
        # (QxT) x A x H
        new_c_feature = torch.matmul(probs, c_feature).squeeze(2)

        new_c_feature = new_c_feature.view(Q, T, A, H)  # batch_size x T x doc_size x hidden_size

        match_logitis = torch.matmul(q_feature.unsqueeze(2), new_c_feature.transpose(2, 3)).squeeze(2)

        match_logitis = torch.log(torch.relu(match_logitis) + 1.0)
        match_logitis = torch.sum(match_logitis, dim=1)
        return match_logitis

    def encode_ans(self, a_input_ids, a_token_type_ids, a_attention_mask):
        a_outs = self.a_bert({'input_ids': a_input_ids, 'token_type_ids': a_token_type_ids, 'input_mask': a_attention_mask})
        a_embedded = a_outs['sentence_embedding']
        return a_embedded

    def encode_que(self, q_ids):
        return self.term_embedding(q_ids)

    def forward(self, q_ids, a_input_ids, a_attention_mask, a_token_type_ids):
        q_embedded = self.encode_que(q_ids)
        a_embedded = self.encode_ans(a_input_ids, a_token_type_ids, a_attention_mask)

        return self._multi_head_cross_similarity(q_embedded, a_embedded)
