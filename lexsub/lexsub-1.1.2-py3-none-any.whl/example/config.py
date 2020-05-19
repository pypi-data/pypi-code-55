import os
emb_dim = '300'
curr_dir = os.path.dirname(__file__)

sem_eval_test = curr_dir + '/data/SEMEVAL07/test/lexsub_test_preprocessed'
sem_eval_test_best = curr_dir + '/semeval_best.out'
sem_eval_test_oot = curr_dir + '/semeval_oot.out'

glove_file = curr_dir + '/embedding/glove.6B/glove.6B.' + emb_dim + 'd.txt'