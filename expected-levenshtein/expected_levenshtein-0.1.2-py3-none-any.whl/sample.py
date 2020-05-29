#!/usr/bin/env python
"""
This module contains functions for the approximate calculation
of expected levenshtein distances between random strings of
various lengths, over alphabets of different sizes.

The expected distances are approximated by averages
over many replicates.
"""

import numpy as np
from numba import njit


@njit
def _lev_jit(a, b):
    """Computes Levenshtein distance between the two
    strings a and b.

    Args:
        a (iterable): String a
        b (iterable): String b

    Returns:
        array_like: the complete distance matrix for a and b
    """
    la, lb = len(a), len(b)
    if la < lb:
        a, b = b, a
        la, lb = lb, la
    L = np.empty(shape=(la + 1, lb + 1))
    for i in range(la + 1):
        for j in range(lb + 1):
            if i == 0:
                L[i, j] = j
            elif j == 0:
                L[i, j] = i
            else:
                h, v, d = L[i - 1, j] + 1, L[i, j - 1] + 1, L[i - 1, j - 1]
                if a[i - 1] != b[j - 1]:
                    d += 1
                L[i, j] = min(d, v, h)
    return L


@njit
def _rand_seq_jit(l, alphabet):
    """Generates a random sequence.

    Args:
        l (int): length of the sequence
        alphabet (array_like): alphabet over which the sequence is built

    Returns:
        array_like: random sequence
    """
    return np.random.choice(alphabet, l)


@njit
def random_average_levenshtein(n, n_samples, alphabet):
    """Compute average levenshtein distances
    of random strings of lengths 1 ≤ length ≤ n
    over <n_samples> samples.

    Args:
        n (int): maximal string length
        n_samples (int): number of samples to generate
        alphabet (array_like): np.array of the alphabet symbols

    Returns:
        array_like: 2D array with the average distances up to length n
    """
    u = _lev_jit(_rand_seq_jit(n, alphabet), _rand_seq_jit(n, alphabet))
    for i in np.arange(2, n_samples + 1):
        sample = _lev_jit(
            _rand_seq_jit(n, alphabet), _rand_seq_jit(n, alphabet))
        u = (i - 1) / i * u + (sample / i)
    return u
