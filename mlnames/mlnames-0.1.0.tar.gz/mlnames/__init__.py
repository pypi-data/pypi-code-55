import os
import random


rng = random.Random()


with open(os.path.join(os.path.dirname(__file__), "corpus"), "r") as f:
    corpus = [vocab.rstrip() for vocab in f.readlines()]

with open(os.path.join(os.path.dirname(__file__), "exclude_words"), "r") as f:
    exclude_words = [w.rstrip() for w in f.readlines()]
exclude_words = set(exclude_words)

corpus = [word for word in corpus if word not in exclude_words]


def set_seed(seed):
    rng.seed(seed)


def get_name(n_words=1, prefix="", suffix="", word_max_len=None):
    if word_max_len is not None:
        filtered_corpus = [word for word in corpus if len(word) <= word_max_len]
    return prefix + "-".join(rng.sample(filtered_corpus, n_words)) + suffix
