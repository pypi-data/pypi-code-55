# @Time    : 9/20/17 2:15 PM
# @Author  : Tiancheng Zhao
import logging
import os
from typing import List
import json
import numpy as np
import scipy.sparse
import torch
from soco_encoders.SentenceTransformer import SentenceTransformer
from tqdm import tqdm
from soco_encoders.models.module_bases import BaseEncoder


class TransformerWrapper(BaseEncoder):
    def __init__(self, model_dir, config):
        super(TransformerWrapper, self).__init__(None, config)
        self.model = SentenceTransformer(model_dir, device='cuda' if config.use_gpu else 'cpu')

        print("Loaded sentence transformer at {}".format(model_dir))

    def forward(self, utts, utt_lens=None, feats=None, return_all=False):
        pass

    def get_dual_sentence_features(self, tokens, start_label, end_label, max_seq_len):
        pad_seq_length = min(max_seq_len + 2, self.model._first_module().max_seq_length)
        tokens = tokens[0:pad_seq_length - 2]

        # first example is on the START and the second example is on the END
        tokens = [self.model._first_module().cls_token_id] + tokens + [self.model._first_module().sep_token_id]
        segment_ids = [0] * len(tokens)
        input_mask = [1] * len(tokens)
        input_ids = tokens
        sentence_length = len(input_ids)

        # PAD TO MAX LEN
        padding_length = pad_seq_length - len(input_ids)
        input_ids = input_ids + ([0] * padding_length)
        input_mask = input_mask + ([0] * padding_length)
        segment_ids = segment_ids + ([0] * padding_length)

        # indicate where the answer is
        segment_ids = np.array(segment_ids)
        segment_ids[start_label:end_label] = 1
        segment_ids = segment_ids.tolist()

        assert len(input_ids) == pad_seq_length
        assert len(input_mask) == pad_seq_length
        assert len(segment_ids) == pad_seq_length

        return {'input_ids': np.asarray(input_ids, dtype=np.int64),
                'token_type_ids': np.asarray(segment_ids, dtype=np.int64),
                'input_mask': np.asarray(input_mask, dtype=np.int64),
                'sentence_lengths': np.asarray(sentence_length, dtype=np.int64)}

    def tokenize_with_brackets(self, tokenize, sent, start_symbol, end_symbol):
        prefix, tokens = sent.split(start_symbol)
        ans, postfix = tokens.split(end_symbol)

        prefix_tokens = tokenize(prefix.strip()) if prefix else []
        ans_tokens = tokenize(ans.strip())
        postfix_tokens = tokenize(postfix.strip()) if postfix else []
        tokens = prefix_tokens + ans_tokens + postfix_tokens

        s_id = len(prefix_tokens)
        ans_len = len(ans_tokens)
        # prediction labels
        start_label = s_id + 1  # CLS token
        end_label = s_id + ans_len + 1  # CLS token

        return tokens, start_label, end_label

    def advanced_encode(self, sentences: List[str], batch_size: int = 8, show_progress_bar: bool = None,
                        start_symbol: str = None, end_symbol: str = None, to_numpy: bool = True,
                        return_mask: bool = False, force_seq_len : int = -1):

        if show_progress_bar is None:
            show_progress_bar = (logging.getLogger().getEffectiveLevel() == logging.INFO
                                 or logging.getLogger().getEffectiveLevel() == logging.DEBUG)

        all_embeddings = []
        all_masks = []
        length_sorted_idx = np.argsort([len(sen) for sen in sentences])

        iterator = range(0, len(sentences), batch_size)
        if show_progress_bar:
            iterator = tqdm(iterator, desc="Batches")

        for batch_idx in iterator:

            batch_start = batch_idx
            batch_end = min(batch_start + batch_size, len(sentences))

            max_seq_len = 0
            batch_tokens = []
            for idx in length_sorted_idx[batch_start:batch_end]:
                tokens, s_id, e_id = self.tokenize_with_brackets(self.model.tokenize, sentences[idx], start_symbol,
                                                                 end_symbol)
                max_seq_len = max(max_seq_len, len(tokens))
                batch_tokens.append((tokens, s_id, e_id))

            features = {}
            for tokens, s_id, e_id in batch_tokens:
                sentence_features = self.get_dual_sentence_features(tokens, s_id, e_id, max(max_seq_len, force_seq_len))

                for feature_name in sentence_features:
                    if feature_name not in features:
                        features[feature_name] = []
                    features[feature_name].append(sentence_features[feature_name])

            for feature_name in features:
                features[feature_name] = torch.tensor(np.asarray(features[feature_name])).to(self.model.device)

            with torch.no_grad():
                embeddings = self.model.forward(features)
                embeddings = embeddings['sentence_embedding']
                mask = features['input_mask']
                if to_numpy:
                    embeddings = embeddings.to('cpu').numpy()
                    mask = mask.to('cpu').numpy()

                all_embeddings.extend(embeddings)
                all_masks.extend(mask)

            if self.use_gpu:
                torch.cuda.empty_cache()

        reverting_order = np.argsort(length_sorted_idx)
        all_embeddings = [all_embeddings[idx] for idx in reverting_order]
        all_masks = [all_masks[idx] for idx in reverting_order]

        if return_mask:
            return all_embeddings, all_masks
        else:
            return all_embeddings

    def encode(self, utts, batch_size=100, show_progress_bar=False, mode=BaseEncoder.DEFAULT, args=None):
        args = dict() if args is None else args
        if mode == BaseEncoder.ANSWER:
            start_symbol = args['start_symbol']
            end_symbol = args['end_symbol']
            embeddings = self.advanced_encode(utts, batch_size=batch_size, show_progress_bar=show_progress_bar,
                                              start_symbol=start_symbol, end_symbol=end_symbol)
        elif mode == BaseEncoder.DEFAULT:
            embeddings = self.model.encode(utts, batch_size=batch_size, show_progress_bar=show_progress_bar)
        else:
            raise Exception("Unsupported mode={} for this encoder".format(mode))

        results = [np.expand_dims(feature, axis=0) for feature in embeddings]
        return np.concatenate(results, axis=0)

    def tokenize_to_ids(self, sent):
        return self.model.tokenize(sent)

    def tokenize_to_pieces(self, sent):
        token_ids = self.model.tokenize(sent)
        return self.model._first_module().tokenizer.convert_ids_to_tokens(token_ids)

    def convert_ids_to_tokens(self, token_ids):
        return self.model._first_module().tokenizer.convert_ids_to_tokens(token_ids)

    def get_embedding_dimension(self):
        return self.model.get_sentence_embedding_dimension()


class TermTransformer(TransformerWrapper):
    logger = logging.getLogger(__name__)

    def __init__(self, model_dir, config):
        super(TermTransformer, self).__init__(model_dir, config)
        self.device = "cuda" if torch.cuda.is_available() and config.use_gpu else "cpu"

        self.term_embedding = torch.load(os.path.join(model_dir, 'term_embeddings.bin'), map_location=self.device)
        self.term_vocab = json.load(open(os.path.join(model_dir, 'term_vocab.json')))

        if config.use_gpu:
            self.logger.info("Use pytorch device: {}".format(self.device))
            self.term_embedding.to(self.device)

        self.log_scale = config.log_scale
        self.score_bias = config.get('score_bias', 0)
        self.max_attention = config.get('max_attention', False)
        self.tokenizer_id = config.get('tokenizer_id', None)
        self.query_tokenize_mode = config.get('query_tokenize_mode', 'char')

    def _multi_head_cross_similarity(self, q_feature, c_feature, q_mask, c_mask, mask_padding=False, approx_padding=False):
        """
        :param q_feature: query_size x T x hidden_size
        :param c_feature: doc_size x num_head x hidden_size
        :param q_mask: query_size x T
        :param c_mask: doc_size x num_token
        :return:
        """
        Q = q_feature.shape[0]
        T = q_feature.shape[1]
        H = q_feature.shape[2]
        A = c_feature.shape[0]
        N = c_feature.shape[1]

        flat_c_feature = c_feature.view(-1, H)
        flat_q_feature = q_feature.view(-1, H)

        head_logits = torch.matmul(flat_q_feature, flat_c_feature.transpose(0, 1))
        logits = head_logits.view(-1, A, N)  # (Q x T) x A x N

        if mask_padding:
            flat_q_mask = q_mask.view(-1, 1)
            flat_c_mask = c_mask[:, 0:N].view(-1, 1)
            logit_mask = torch.matmul(flat_q_mask, flat_c_mask.transpose(0, 1))
            logit_mask = (1.0 - logit_mask) * -10000.0
            logit_mask = logit_mask.view(-1, A, N)
            logits += logit_mask

        if self.max_attention:
            max_logitis, _ = torch.max(logits, dim=2)
            match_logitis = max_logitis.view(Q, T, A)
        else:
            probs = torch.softmax(logits, dim=2).unsqueeze(2)  # (QxT)x A x 1 x N
            new_c_feature = torch.matmul(probs, c_feature).squeeze(2)  # (QxT) x A x H

            new_c_feature = new_c_feature.view(Q, T, A, H)  # batch_size x T x doc_size x hidden_size
            match_logitis = torch.matmul(q_feature.unsqueeze(2), new_c_feature.transpose(2, 3)).squeeze(2)

            if approx_padding:
                seq_len = torch.sum(c_mask, dim=1)
                match_logitis += torch.clamp((seq_len * (1 / 320) - 1).view(1, 1, -1), max=0.0)

        match_logitis = match_logitis + self.score_bias

        match_logitis = torch.relu(match_logitis)
        if self.log_scale:
            match_logitis = torch.log(match_logitis + 1.0)

        match_logitis = torch.sum(match_logitis, dim=1)
        return match_logitis

    def _top_p(self, matrix, p):
        """
        :param matrix: num_sent x num_terms
        :param p: [0 to 1]
        :return:
        """
        sorted_matrix = np.sort(matrix * -1, axis=1) * -1
        p_matrix = np.cumsum(sorted_matrix, axis=1) / np.sum(matrix, axis=1, keepdims=True)
        result = np.array(matrix, copy=True)
        for row_id in range(matrix.shape[0]):
            th = 0
            for col_id in range(matrix.shape[1]):
                th = sorted_matrix[row_id, col_id]
                if p_matrix[row_id, col_id] >= p:
                    break

            row = matrix[row_id]
            row[row < th] = 0.0
            result[row_id] = row

        return result

    def _top_k(self, matrix, k):
        sorted_matrix = np.sort(matrix * -1, axis=1) * -1
        result = np.array(matrix, copy=True)
        for row_id in range(matrix.shape[0]):
            th = sorted_matrix[row_id][k]

            row = matrix[row_id]
            row[row < th] = 0.0
            result[row_id] = row

        return result

    def _clamp(self, matrix, min_threshold):
        """
        :param matrix: num_sent x num_terms
        :param p: [0 to 1]
        :return:
        """
        matrix[matrix <= min_threshold] = 0.0
        return matrix

    def encode(self, sentences, batch_size=100, show_progress_bar=False, mode=BaseEncoder.TSCORE, args=None):

        if mode != BaseEncoder.TSCORE:
            raise Exception("Unsupported mode={} for this encoder".format(mode))

        args = dict() if args is None else args
        start_symbol = args.get('start_symbol', None)
        end_symbol = args.get('end_symbol', None)
        top_p = args.get('top_p', None)
        top_k = args.get('top_k', None)
        min_threshold = args.get('min_threshold', None)
        return_meta = args.get('return_meta', False)
        to_sparse = args.get('to_sparse', None)
        term_batch_size = args.get('term_batch_size', 1000)
        force_seq_len = args.get('force_seq_len', -1)
        mask_padding = args.get('mask_padding', True)
        approx_padding = args.get('approx_padding', False)

        vocab_size = self.term_embedding.num_embeddings
        all_term_scores = []
        length_sorted_idx = np.argsort([len(sen) for sen in sentences])

        iterator = range(0, len(sentences), batch_size)
        if show_progress_bar:
            iterator = tqdm(iterator, desc="Batches")

        with torch.no_grad():

            for batch_idx in iterator:
                batch_start = batch_idx
                batch_end = min(batch_start + batch_size, len(sentences))
                batch = [sentences[idx] for idx in length_sorted_idx[batch_start:batch_end]]

                if start_symbol is not None and end_symbol is not None:
                    embeddings, masks = self.advanced_encode(batch, batch_size=batch_size, show_progress_bar=False,
                                                             start_symbol=start_symbol, end_symbol=end_symbol,
                                                             to_numpy=False, return_mask=True,
                                                             force_seq_len=force_seq_len)

                    embeddings = torch.cat([e.unsqueeze(0) for e in embeddings], dim=0)
                    masks = torch.cat([e.unsqueeze(0) for e in masks], dim=0)
                else:
                    raise Exception("Currently default encoding is not supported yet")

                # compute term wise weights
                s_id = 0
                e_id = min(s_id + term_batch_size, vocab_size)
                temp_loigits = []
                while True:
                    terms = torch.arange(s_id, e_id).long().to(self.device)
                    term_vectors = self.term_embedding(terms).unsqueeze(1)
                    temp = self._multi_head_cross_similarity(term_vectors, embeddings,
                                                             q_mask=torch.ones(term_vectors.size()[0:2]).to(self.device),
                                                             c_mask=masks.float(),
                                                             mask_padding=mask_padding,
                                                             approx_padding = approx_padding
                                                             )
                    temp_loigits.append(temp.detach().cpu().transpose(0, 1).numpy())
                    if e_id >= vocab_size:
                        break

                    s_id = e_id
                    e_id = min(s_id + term_batch_size, vocab_size)

                temp_loigits = np.concatenate(temp_loigits, axis=1)
                all_term_scores.append(temp_loigits)

        reverting_order = np.argsort(length_sorted_idx)
        all_term_scores = np.concatenate(all_term_scores, axis=0)
        all_term_scores = [all_term_scores[idx] for idx in reverting_order]
        all_term_scores = np.array(all_term_scores)
        nz_count = np.count_nonzero(all_term_scores)
        logging.info("Encoding non-zero rate {:.3f}".format(nz_count / float(all_term_scores.size)))

        if top_p is not None:
            all_term_scores = self._top_p(all_term_scores, top_p)
            nz_count = np.count_nonzero(all_term_scores)
            self.logger.info("Top p={} non-zero rate {:.3f}".format(top_p, nz_count / float(all_term_scores.size)))

        if top_k is not None:
            all_term_scores = self._top_k(all_term_scores, top_k)
            nz_count = np.count_nonzero(all_term_scores)
            self.logger.info("Top k={} non-zero rate {:.3f}".format(top_k, nz_count / float(all_term_scores.size)))

        if min_threshold is not None:
            all_term_scores = self._clamp(all_term_scores, min_threshold)
            nz_count = np.count_nonzero(all_term_scores)
            self.logger.info(
                "Min threshold={} non-zero rate {:.3f}".format(min_threshold, nz_count / float(all_term_scores.size)))

        if to_sparse is not None:
            if to_sparse == 'csr':
                all_term_scores = scipy.sparse.csr_matrix(all_term_scores)
            elif to_sparse == 'coo':
                all_term_scores = scipy.sparse.coo_matrix(all_term_scores)
            elif to_sparse == 'dok':
                all_term_scores = scipy.sparse.dok_matrix(all_term_scores)
            else:
                self.logger.warning("Unknown sparse format {}".format(to_sparse))

        if return_meta:
            return all_term_scores, {'vocab': self.term_vocab}
        else:
            return all_term_scores

