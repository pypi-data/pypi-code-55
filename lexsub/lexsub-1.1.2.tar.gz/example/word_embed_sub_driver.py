from lexsub.process_data.definition import LexSubExample
import nltk
import sys
import os
import argparse


nltk.download('words')

sys.path.append(os.path.dirname(__file__) + '../')

emb_dim = '300'
curr_dir = os.path.dirname(__file__)

sem_eval_test = curr_dir + '/data/SEMEVAL07/test/lexsub_test_preprocessed'
sem_eval_test_best = curr_dir + '/semeval_best.out'
sem_eval_test_oot = curr_dir + '/semeval_oot.out'

glove_file = curr_dir + '/embedding/glove.6B/glove.6B.' + emb_dim + 'd.txt'

if __name__ == '__main__':
    tfi = open(sem_eval_test, 'r', encoding='iso8859')
    for line in tfi:
        # Process / Read Lines
        segments = line.split('\t')
        data_point = LexSubExample(key=segments[0],
                                   idx=segments[1],
                                   word_pos=int(segments[2]),
                                   context=segments[3])