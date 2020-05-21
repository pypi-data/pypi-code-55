import argparse
import os
import sys

import nltk
import tqdm
from nltk.corpus import words

import config as conf
from lexsub import BERTLexSub, LexSubUtils, DataReader

nltk.download('words')

sys.path.append(os.path.dirname(__file__) + '../')


def _parse_args():
    parser = argparse.ArgumentParser(description='bert_sub_driver.py')
    parser.add_argument('--d', type=str, default='SEMEVAL',
                        help='Pass Data-set| Options: SEMEVAL, ')
    parser.add_argument('--m', type=str, default='BertModel',
                        help='Model Type: Options: https://huggingface.co/transformers/pretrained_models.html')
    parser.add_argument('--w', type=str, default='bert-base-uncased',
                        help='PreTrained Weight: Options: https://huggingface.co/transformers/pretrained_models.html')
    parser.add_argument('--i', type=str, default=conf.sem_eval_test,
                        help='best o/p file')
    parser.add_argument('--b', type=str, default=conf.sem_eval_test_best,
                        help='best o/p file')
    parser.add_argument('--o', type=str, default=conf.sem_eval_test_oot,
                        help='oot o/p file')
    parser.add_argument('--k', type=int, default=20,
                        help='no of proposal candidate')
    args = parser.parse_args()
    return args


def run_experiment(args):
    # Masked LM Candidate -> Word Affinity Based Filtering
    data_set = args.d
    model_class = args.m
    pre_trained_wt = args.w

    in_file = args.i
    best_out = args.b
    oot_out = args.o
    k = args.k

    # ------------------------ Read Data Set --------------------------
    tfi = open(in_file, 'r', encoding='iso8859')
    tfo_best = open(best_out, 'w+')
    tfo_oot = open(oot_out, 'w+')
    data_reader = DataReader(fi=tfi, data_set=data_set, embedding_file=conf.glove_file)

    # ------------------------ Masked LM Candidate Set Generation --------------------------
    feasible_set = set(words.words())
    tokenizer, masked_lm = LexSubUtils().fetch_pre_trained(model_class=model_class, pre_trained_wt=pre_trained_wt)

    for data_point in tqdm.tqdm(data_reader.data_points, total=data_reader.num_lines):
        # Forward Pass through Pre-trained Model - predicts masked token using LM objective P(x_k|x') where
        # x' is the sentence with the k th token masked
        bert_candidate = BERTLexSub(example=data_point,
                                    masked_lm=masked_lm,
                                    tokenizer=tokenizer,
                                    model_class=model_class,
                                    k=k,
                                    feasible_set=feasible_set)
        lm_pred_candidates = bert_candidate.masked_lm_prediction()

        # Now go through the candidates and compute word embedding sim score w.r.t. target word
        for lm_candidate in lm_pred_candidates:
            emb_candidate = data_reader.embed_lookup.get_word_embedding(word=lm_candidate.token)
            emb_target = data_reader.embed_lookup.get_word_embedding(word=data_point.target_word)
            lm_candidate.static_word_sim = data_reader.embed_lookup.get_similarity_score(vec_1=emb_candidate,
                                                                                         vec_2=emb_target,
                                                                                         measure='cosine')

        # normalize each scores
        sum_lm = 0
        sum_word_sim = 0

        for c in lm_pred_candidates:
            sum_lm += c.lm_score
            sum_word_sim += c.static_word_sim

        for c in lm_pred_candidates:
            c.lm_score = c.lm_score / sum_lm
            c.static_word_sim = c.static_word_sim / sum_word_sim

        # re-rank list
        lm_pred_candidates.sort(key=lambda x: x.ranking_score, reverse=True)

        # return the top 10 only
        pred_candidates = lm_pred_candidates[0:10]
        # ------------------------ Process / Write results --------------------------
        tfo_best.write(' '.join([data_point.key, data_point.id]) + " :: "
                       + pred_candidates[0].token + "\n")
        tokens = []
        for candidate in pred_candidates:
            tokens.append(candidate.token)
        tfo_oot.write(' '.join([data_point.key, data_point.id]) + " ::: "
                      + ';'.join(tokens) + "\n")


if __name__ == '__main__':
    args = _parse_args()
    print(args)
    run_experiment(args)
